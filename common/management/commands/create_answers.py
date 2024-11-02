import faker
from django.core.management import BaseCommand
from common.models import Question, Subjects, Examine

fake = faker.Faker()


class Command(BaseCommand):
    help = "100 ta tasodifiy savol yaratish"

    def handle(self, *args, **kwargs):
        subject = Subjects.objects.first()
        if not subject:
            self.stdout.write(self.style.ERROR("Hech qanday subject mavjud emas. Avval subject yarating."))
            return

        examine = Examine.objects.filter(subjects=subject).first()
        if not examine:
            self.stdout.write(self.style.ERROR("Hech qanday imtihon mavjud emas. Avval imtihon yarating."))
            return

        for _ in range(100):
            options = [
                {"label": "A", "text": fake.sentence()},
                {"label": "B", "text": fake.sentence()},
                {"label": "C", "text": fake.sentence()},
                {"label": "D", "text": fake.sentence()}
            ]

            correct_option = options[fake.random_int(0, 3)]["label"]

            Question.objects.create(
                subject=subject,
                body=fake.text(max_nb_chars=200),
                correct_answer=correct_option,
                options=options,
                type="Multiple Choice"
            )

        self.stdout.write(self.style.SUCCESS("100 ta tasodifiy savol yaratildi."))
