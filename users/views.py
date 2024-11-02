from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.cache import cache

from users.serializers import RegisterSerializer, VerificationEmailSerializers, LoginSerializer, \
    ChangeUserModelSerializer, ForgotChangeUserModelSerializer, ForgotPasswordModelSerializer
from users.task import generate_verification_code, send_forgot_password_email

from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, VerificationEmailSerializers
from .task import send_verification_email, generate_verification_code
from .models import User


class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            status.HTTP_201_CREATED: "User successfully registered",
            status.HTTP_400_BAD_REQUEST: "Invalid Credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            email = serializer.validated_data['email']
            verification_code = generate_verification_code()
            expire_time = timezone.now() + timedelta(minutes=10)

            user = User.objects.get(email=email)
            user.verification_code = verification_code
            user.activation_key_expires = expire_time
            user.save()

            send_verification_email.delay(to_email=email, verification_code=verification_code)

            return Response("Emailga tasdiqlash kodi yuborildi, iltimos tasdiqlab yuboring",
                            status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    serializer_class = VerificationEmailSerializers

    @swagger_auto_schema(
        request_body=VerificationEmailSerializers,
        responses={
            status.HTTP_200_OK: "Email tasdiqlandi",
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            verification_code = serializer.validated_data.get("verification_code")

            try:
                instance = User.objects.get(email=email, verification_code=verification_code)

                if not instance.is_verified and instance.activation_key_expires > timezone.now():
                    instance.is_active = True
                    instance.is_verified = True
                    instance.save()
                    return Response({"message": "Email tasdiqlandi"}, status=status.HTTP_200_OK)

                elif instance.is_verified:
                    return Response({"message": "Email allaqachon tasdiqlangan."}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"message": "Tasdiqlash kodi eskirgan yoki noto'g'ri"},
                                    status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response({"message": "Noto'g'ri tasdiqlash kod yoki email"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: "Login successfully",
            status.HTTP_400_BAD_REQUEST: "Invalid Credentials",
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            user = cache.get(f'user_{email}')
            if not user:
                user = authenticate(username=email, password=password)
                if user:
                    cache.set(f'user_{email}', user, timeout=300)
            if user and user.is_verified is True:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "detail": "Successfully login",
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }, status=status.HTTP_200_OK)

            return Response({"detail": "Xato email yoki password"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    @swagger_auto_schema(
        request_body=ForgotPasswordModelSerializer,
        responses={
            status.HTTP_200_OK: "Parolni tiklash uchun tasdiqlash kodi jo'natildi.",
            status.HTTP_404_NOT_FOUND: "Foydalanuvchi topilmadi.",
        }
    )
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            verification_code = generate_verification_code()
            expiration_time = timezone.now() + timedelta(minutes=1)
            user.verification_code = verification_code
            user.activation_key_expires = expiration_time
            user.save()

            # Log to debug email sending
            send_forgot_password_email(to_email=email, verification_code=verification_code)
            return Response({"message": "Parolni tiklash uchun tasdiqlash kodi jo'natildi."},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'Foydalanuvchi email manzili topilmadi.'},
                            status=status.HTTP_404_NOT_FOUND)


class VerifyForgotEmailView(APIView):
    @swagger_auto_schema(
        request_body=ForgotChangeUserModelSerializer,
        responses={
            status.HTTP_200_OK: "Email tasdiqlandi va parol o'zgardi.",
            status.HTTP_400_BAD_REQUEST: "Tasdiqlash kod muddati tugagan yoki noto'g'ri tasdiqlash kod.",
            status.HTTP_404_NOT_FOUND: "Noto'g'ri tasdiqlash kod yoki email.",
        },
    )
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        verification_code = request.data.get('verification_code')

        try:
            user = User.objects.get(email=email, verification_code=verification_code)

            # Check if verification code is valid and not expired
            if user.activation_key_expires > timezone.now():
                if new_password != confirm_password:
                    return Response({'message': 'Parol va tasdiqlash mos kelmadi.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Set new password and mark as verified
                user.set_password(new_password)
                user.is_verified = True
                user.save()
                return Response(data={'message': "Email tasdiqlandi va parol o'zgardi"},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Tasdiqlash kod muddati tugagan yoki noto\'g\'ri tasdiqlash kod.'},
                                status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'message': 'Noto\'g\'ri tasdiqlash kod yoki email.'}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChangeUserModelSerializer,
        responses={
            200: 'Password successfully changed',
            400: 'Bad Request',
            401: 'Unauthorized',
        }
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'Foydalanuvchi autentifikatsiya qilinmagan.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChangeUserModelSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            user = request.user

            if user.is_verified:
                user.set_password(password)
                user.save()

                cache.delete(f'user_{user.id}')  # Foydalanuvchi ma'lumotlarini keshdan olib tashlash

                return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Foydalanuvchi emailni tasdiqlamagan.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
