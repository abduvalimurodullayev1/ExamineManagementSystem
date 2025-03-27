from rest_framework.permissions import BasePermission

from apps.users.models import User


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ReleCHOICES.TEACHER

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.ReleCHOICES.TEACHER

