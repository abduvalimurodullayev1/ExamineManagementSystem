from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import signals
from django.dispatch import receiver
from django.db.models import Sum, Avg, Max, Min, Count

from apps.users.models import BaseModel


class Subjects(BaseModel):
    slug = models.SlugField(verbose_name=_("Slug"), unique=True)
    title = models.CharField(max_length=122, verbose_name=_("Title"), unique=True)
    description = models.TextField(max_length=500, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return self.title


class Exam(models.Model):
    class ExamStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        DRAFT = "draft", _("Draft")
        FINISHED = "finished", _("Finished")

    class ExamTypes(models.TextChoices):
        MCQ = "mcq", _("Multiple Choice")
        ESSAY = "essay", _("Essay")
        MIXED = "mixed", _("Mixed")

    exam_type = models.CharField(max_length=20, choices=ExamTypes, default=ExamTypes.MCQ, verbose_name=_("Exam Type"))
    status = models.CharField(max_length=10, choices=ExamStatus.choices, default=ExamStatus.DRAFT, verbose_name=_("Status"))
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Duration (minutes)"))
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    start_time = models.DateTimeField(verbose_name=_("Start time"))
    end_time = models.DateTimeField(null=True, blank=True, verbose_name=_("End time"))
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_("Created by"))
    max_score = models.PositiveIntegerField(verbose_name=_("Max Score"), default=100)
    calculated_total_score = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Calculated Total Score"))
    questions = models.ManyToManyField("Question", through="QuestionScore", verbose_name=_("Questions"), blank=True)
    attempt_limit = models.PositiveIntegerField(default=1, verbose_name=_("Attempt Limit"), help_text=_("0 for unlimited attempts"))
    passing_score = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Passing Score"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is Published"))
    is_timed = models.BooleanField(default=True, verbose_name=_("Is Timed"))
    randomize_questions = models.BooleanField(default=False, verbose_name=_("Randomize Questions"))
    tags = models.CharField(max_length=255, blank=True, verbose_name=_("Tags"), help_text=_("Comma-separated tags"))

    def clean(self):
        if self.is_timed and (self.duration is None or self.duration <= 0):
            raise ValidationError(_("Duration must be positive when exam is timed."))
        if self.status == self.ExamStatus.DRAFT and self.start_time < timezone.now():
            raise ValidationError(_("Start time cannot be in the past for a draft exam."))
        if self.passing_score is not None and self.passing_score > self.max_score:
            raise ValidationError(_("Passing score cannot exceed max score."))

    def save(self, *args, **kwargs):
        if self.is_timed and self.duration:
            from datetime import timedelta
            self.end_time = self.start_time + timedelta(minutes=self.duration)
        else:
            self.end_time = None
        super().save(*args, **kwargs)

    def update_calculated_total_score(self):
        if self.questions.exists():
            total = QuestionScore.objects.filter(exam=self).aggregate(total=Sum('score'))['total'] or 0
            self.calculated_total_score = total
            if total != self.max_score:
                raise ValidationError(_("Total score of questions (%s) does not match max_score (%s)." % (total, self.max_score)))
        else:
            self.calculated_total_score = 0
        self.save(update_fields=['calculated_total_score'])

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'status']),
            models.Index(fields=['subject', 'created_by']),
        ]
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")

    def __str__(self):
        return f"{self.subject.title} - {self.start_time}"


class Question(models.Model):
    class QuestionTypes(models.TextChoices):
        MCQ = "mcq", _("Multiple Choice")
        ESSAY = "essay", _("Essay")
        TRUE_FALSE = "true_false", _("True/False")
        SHORT_ANSWER = "short_answer", _("Short Answer")

    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    body = models.TextField(verbose_name=_("Question Body"))
    correct_answer = models.TextField(verbose_name=_("Correct Answer"), blank=True, null=True)
    options = models.JSONField(verbose_name=_("Options"), blank=True, null=True, help_text=_("JSON format: [{'id': 1, 'text': 'Option A'}, ...]"))
    type = models.CharField(max_length=50, choices=QuestionTypes, default=QuestionTypes.MCQ, verbose_name=_("Type"))
    difficulty_level = models.PositiveSmallIntegerField(default=1, verbose_name=_("Difficulty Level"), help_text=_("1-5 scale"))

    def clean(self):
        if self.type == self.QuestionTypes.MCQ and (not self.options or not self.correct_answer):
            raise ValidationError(_("Multiple Choice questions must have options and a correct answer."))
        if self.type == self.QuestionTypes.ESSAY and (self.options or self.correct_answer):
            raise ValidationError(_("Essay questions should not have options or a correct answer."))
        if self.type == self.QuestionTypes.TRUE_FALSE and self.correct_answer not in ["true", "false", None]:
            raise ValidationError(_("True/False questions must have 'true' or 'false' as correct answer."))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        indexes = [models.Index(fields=['subject', 'type'])]

    def __str__(self):
        return self.body[:50]


class QuestionScore(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Question"))
    score = models.PositiveIntegerField(verbose_name=_("Score"), default=1)
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        unique_together = ('question', 'exam')
        indexes = [models.Index(fields=['exam', 'order'])]
        verbose_name = _("Question Score")
        verbose_name_plural = _("Question Scores")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.exam.update_calculated_total_score()


class Submission(models.Model):
    class SubmissionStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SUBMITTED = "submitted", _("Submitted")
        EVALUATED = "evaluated", _("Evaluated")

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    student = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("Student"))
    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Started At"))
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name=_("Submitted At"))
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Finished At"))
    answers = models.JSONField(verbose_name=_("Answers"), help_text=_("Format: {question_id: answer}"))
    score = models.FloatField(verbose_name=_("Score"), null=True, blank=True)
    status = models.CharField(max_length=20, choices=SubmissionStatus.choices, default=SubmissionStatus.DRAFT, verbose_name=_("Status"))
    feedback = models.TextField(blank=True, null=True, verbose_name=_("Feedback"))
    evaluated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Evaluated by"), related_name="evaluated_submissions")
    attempt_number = models.PositiveIntegerField(default=1, verbose_name=_("Attempt Number"))
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True, blank=True, verbose_name=_("Submitted File"))

    def calculate_score(self):
        total_score = 0
        question_scores = QuestionScore.objects.filter(exam=self.exam).select_related('question')
        for qs in question_scores:
            if qs.question.type == Question.QuestionTypes.MCQ:
                student_answer = self.answers.get(str(qs.question.id))
                if student_answer == qs.question.correct_answer:
                    total_score += qs.score
            elif qs.question.type == Question.QuestionTypes.TRUE_FALSE:
                student_answer = self.answers.get(str(qs.question.id))
                if student_answer == qs.question.correct_answer:
                    total_score += qs.score
        self.score = total_score
        self.status = self.SubmissionStatus.SUBMITTED
        self.save(update_fields=['score', 'status'])

    class Meta:
        unique_together = ('exam', 'student', 'attempt_number')
        indexes = [
            models.Index(fields=['student', 'submitted_at']),
            models.Index(fields=['exam', 'status']),
        ]
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")

    def __str__(self):
        return f"{self.student.username} - {self.exam.subject} (Attempt {self.attempt_number})"


class ExamGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    students = models.ManyToManyField('users.User', verbose_name=_("Students"))
    exams = models.ManyToManyField(Exam, verbose_name=_("Exams"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Exam Group")
        verbose_name_plural = _("Exam Groups")

    def __str__(self):
        return self.name


class ExamStatistics(models.Model):
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    average_score = models.FloatField(default=0, verbose_name=_("Average Score"))
    highest_score = models.FloatField(default=0, verbose_name=_("Highest Score"))
    lowest_score = models.FloatField(default=0, verbose_name=_("Lowest Score"))
    participants = models.PositiveIntegerField(default=0, verbose_name=_("Participants"))

    class Meta:
        verbose_name = _("Exam Statistics")
        verbose_name_plural = _("Exam Statistics")

    def __str__(self):
        return f"Stats for {self.exam}"


