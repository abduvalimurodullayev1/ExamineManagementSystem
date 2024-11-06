from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
import random

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Subjects(models.Model):
    title = models.CharField(max_length=122, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.title


class Question(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    body = models.TextField(verbose_name=_("Question Body"))
    correct_answer = models.CharField(verbose_name=_("Correct Answer"), max_length=100)
    options = models.JSONField(verbose_name=_("Options"))
    type = models.CharField(max_length=50, verbose_name=_("Type"), default="Multiple Choice")

    def __str__(self):
        return f"{self.body[:50]}..."

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class Examine(models.Model):
    subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    exam_name = models.CharField(max_length=100, verbose_name=_("Exam name"))
    start_time = models.DateTimeField(verbose_name=_("Start time"))
    end_time = models.DateTimeField(verbose_name=_("End time"))
    question_count = models.PositiveIntegerField(verbose_name=_("Question count"))
    passing_percentage = models.PositiveIntegerField(verbose_name=_("Passing percentage"), default=50)
    total_score = models.PositiveIntegerField(verbose_name=_("Total score"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    assigned_users = models.ManyToManyField(User, related_name="assigned_exams", verbose_name=_("Assigned users"),
                                            blank=True)
    questions = models.ManyToManyField(Question, related_name="exams", verbose_name=_("Questions"), blank=True)

    class Meta:
        verbose_name = _("Examine")
        verbose_name_plural = _("Examines")

    def __str__(self):
        return self.exam_name

    def calculate_score(self, student):
        submissions = Submission.objects.filter(student=student, exam=self)
        correct_answers = submissions.filter(is_correct=True).count()
        total_questions = self.questions.count()

        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        return score_percentage

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.questions.exists():
            all_questions = list(Question.objects.filter(subject=self.subjects))
            selected_questions = random.sample(all_questions, min(len(all_questions), self.question_count))
            self.questions.set(selected_questions)


class ExamResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Student"))
    exam = models.ForeignKey(Examine, on_delete=models.CASCADE, verbose_name=_("Exam"))
    score = models.PositiveIntegerField(verbose_name=_("Score"))
    passed = models.BooleanField(default=False, verbose_name=_("Passed"))

    class Meta:
        verbose_name = _("ExamResult")
        verbose_name_plural = _("ExamResults")

    def calculate_and_save_result(self):
        score_percentage = self.exam.calculate_score(self.student)

        exam_result, created = ExamResult.objects.get_or_create(student=self.student, exam=self.exam)
        exam_result.score = score_percentage
        exam_result.passed = score_percentage >= self.exam.passing_percentage
        exam_result.save()


class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Student"))
    exam = models.ForeignKey(Examine, on_delete=models.CASCADE, verbose_name=_("Exam"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Question"))
    answer = models.CharField(max_length=100, verbose_name=_("Answer"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Is correct"))  # Qo'shilgan maydon

    def save(self, *args, **kwargs):
        self.is_correct = (self.answer == self.question.correct_answer)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.exam.exam_name} - {self.question.body[:50]}..."

    class Meta:
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")


class Assignment(BaseModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments", verbose_name=_("Student"))
    exam = models.ForeignKey(Examine, on_delete=models.CASCADE, related_name="assignments", verbose_name=_("Exam"))
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Assigned at"))
    completed = models.BooleanField(default=False, verbose_name=_("Completed"))
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Completion Date"))

    class Meta:
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    message = models.TextField(verbose_name=_("Message"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))
    is_sent = models.BooleanField(default=False, verbose_name=_("Is Sent"))
