from django.core.management.base import BaseCommand
from common.models import Examine, Subjects
from django.utils import timezone
import random
from datetime import timedelta


class Command(BaseCommand):
    help = "Examine yaratish"

    def handle(self, *args, **options):
        subjects = Subjects.objects.first()
        if not subjects:
            self.stdout.write(self.style.ERROR("Hech qanday subject mavjud emas"))
            return

        for i in range(10):
            # Imtihon uchun boshlanish va tugash vaqtlarini tasodifiy belgilash
            start_time = timezone.now() + timedelta(days=i)
            end_time = start_time + timedelta(hours=2)  # 2 soatdan so'ng tugaydi

            # Examine ob'ekti yaratish
            Examine.objects.create(
                subjects=subjects,
                exam_name=f"Exam {i + 1}",
                start_time=start_time,
                end_time=end_time,
                question_count=random.randint(5, 20),  # 5 dan 20 gacha savollar
                passing_percentage=random.randint(50, 100),  # 50% dan 100% gacha
                total_score=random.randint(100, 200),
                active=True
            )
            self.stdout.write(self.style.SUCCESS(f"Examine {i + 1} yaratildi!"))
