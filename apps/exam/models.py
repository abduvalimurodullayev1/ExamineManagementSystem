from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel


class Subjects(BaseModel):
    title = models.CharField(max_length=122, verbose_name=_("Title"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.title


class Exam(BaseModel):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    start_time = models.DateTimeField(verbose_name=_("Start time"))
    end_time = models.DateTimeField(verbose_name=_("End time"))


class Question(BaseModel):
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


















