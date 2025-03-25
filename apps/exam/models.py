from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


class Subjects(models.Model):
    title = models.CharField(max_length=122, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.title


class Exam(models.Model):
    class ExamStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        DRAFT = "draft", _("Draft")
        FINISHED = "finished", _("Finished")

    EXAM_TYPES = (
        ('mcq', 'Multiple Choice'),
        ('essay', 'Essay'),
        ('mixed', 'Mixed'),
    )
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='mcq', verbose_name=_("Exam Type"))
    status = models.CharField(max_length=10, choices=ExamStatus.choices, verbose_name=_("Status"))
    duration = models.PositiveIntegerField(verbose_name=_("Duration"))
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    start_time = models.DateTimeField(verbose_name=_("Start time"))
    end_time = models.DateTimeField(verbose_name=_("End time"))
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_("Created by"))
    max_score = models.PositiveIntegerField(verbose_name=_("Max score"))
    questions = models.ManyToManyField("Question", verbose_name=_("Questions"), blank=True)

    def clean(self):
        if self.start_time < self.end_time:
            raise ValidationError("Start time must be before end time.")
        if self.duration <= 0:
            raise ValidationError("Duration cannot be negative.")

    class Meta:
        indexes = [models.Index(fields=['start_time', 'status'])]


class Question(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    body = models.TextField(verbose_name=_("Question Body"))
    correct_answer = models.CharField(verbose_name=_("Correct Answer"), max_length=100)
    options = models.JSONField(verbose_name=_("Options"))
    type = models.CharField(max_length=50, verbose_name=_("Type"), default="Multiple Choice")

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.body


class Submission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    student = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("Student"))
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name=_("Submitted At"))
