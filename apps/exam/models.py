from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum, Avg, Max, Min, Count, Q
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

from apps.common.models import BaseModel


class Subjects(BaseModel):
    slug = models.SlugField(verbose_name=_("Slug"), unique=True)
    title = models.CharField(max_length=122, verbose_name=_("Title"), unique=True)
    description = models.TextField(max_length=500, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        indexes = [models.Index(fields=['slug', 'title'])]

    def __str__(self):
        return self.title


class Exam(models.Model):
    class ExamStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SCHEDULED = "scheduled", _("Scheduled")
        ACTIVE = "active", _("Active")
        FINISHED = "finished", _("Finished")

    class ExamTypes(models.TextChoices):
        MCQ = "mcq", _("Multiple Choice")
        ESSAY = "essay", _("Essay")
        MIXED = "mixed", _("Mixed")
        PRACTICAL = "practical", _("Practical")

    exam_type = models.CharField(max_length=20, choices=ExamTypes, default=ExamTypes.MCQ, verbose_name=_("Exam Type"))
    status = models.CharField(max_length=10, choices=ExamStatus.choices, default=ExamStatus.DRAFT,
                              verbose_name=_("Status"))
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Duration (minutes)"))
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(null=True, blank=True, verbose_name=_("End Time"))
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_("Created by"))
    max_score = models.PositiveIntegerField(verbose_name=_("Max Score"), default=100)
    calculated_total_score = models.PositiveIntegerField(null=True, blank=True,
                                                         verbose_name=_("Calculated Total Score"))
    questions = models.ManyToManyField("Question", through="QuestionScore", verbose_name=_("Questions"), blank=True)
    attempt_limit = models.PositiveIntegerField(default=1, verbose_name=_("Attempt Limit"),
                                                help_text=_("0 for unlimited"))
    passing_score = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Passing Score"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is Published"))
    is_timed = models.BooleanField(default=True, verbose_name=_("Is Timed"))
    randomize_questions = models.BooleanField(default=False, verbose_name=_("Randomize Questions"))
    tags = models.CharField(max_length=255, blank=True, verbose_name=_("Tags"), help_text=_("Comma-separated tags"))
    instructions = models.TextField(blank=True, verbose_name=_("Instructions"))

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
        total = QuestionScore.objects.filter(exam=self).aggregate(total=Sum('score'))['total'] or 0
        self.calculated_total_score = total
        if total != self.max_score:
            raise ValidationError(
                _("Total score of questions (%s) does not match max_score (%s)." % (total, self.max_score)))
        self.save(update_fields=['calculated_total_score'])

    def is_active(self):
        now = timezone.now()
        return self.status == self.ExamStatus.ACTIVE and self.start_time <= now <= (self.end_time or now)

    def update_status(self):
        now = timezone.now()
        if now < self.start_time:
            self.status = self.ExamStatus.SCHEDULED
        elif self.start_time <= now <= (self.end_time or now):
            self.status = self.ExamStatus.ACTIVE
        else:
            self.status = self.ExamStatus.FINISHED
        self.save(update_fields=['status'])

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'status']),
            models.Index(fields=['subject', 'created_by']),
            models.Index(fields=['is_published', 'exam_type']),
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
        MATCHING = "matching", _("Matching")

    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    body = models.TextField(verbose_name=_("Question Body"))
    type = models.CharField(max_length=50, choices=QuestionTypes, default=QuestionTypes.MCQ, verbose_name=_("Type"))
    difficulty_level = models.PositiveSmallIntegerField(default=1, verbose_name=_("Difficulty Level"),
                                                        help_text=_("1-5 scale"))
    attachment = models.FileField(upload_to='questions/%Y/%m/%d/', null=True, blank=True, verbose_name=_("Attachment"))

    def clean(self):
        if self.type == self.QuestionTypes.MCQ:
            options = self.options.all()  # related_name='options'
            if len(options) < 2:
                raise ValidationError(_("MCQ must have at least 2 options."))
            correct_count = sum(1 for opt in options if opt.is_correct)
            if correct_count != 1:
                raise ValidationError(_("MCQ must have exactly one correct option."))
        elif self.type == self.QuestionTypes.ESSAY and self.options.exists():
            raise ValidationError(_("Essay questions cannot have options."))


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', verbose_name=_("Question"))
    option_text = models.CharField(max_length=255, verbose_name=_("Option Text"))
    is_correct = models.BooleanField(default=False, verbose_name=_("Is Correct"))

    class Meta:
        verbose_name = _("Question Option")
        verbose_name_plural = _("Question Options")

    def __str__(self):
        return self.option_text


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
        PENDING_EVALUATION = "pending_evaluation", _("Pending Evaluation")
        EVALUATED = "evaluated", _("Evaluated")

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    student = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("Student"))
    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Started At"))
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name=_("Submitted At"))
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Finished At"))
    score = models.FloatField(verbose_name=_("Score"), null=True, blank=True)
    status = models.CharField(max_length=20, choices=SubmissionStatus.choices, default=SubmissionStatus.DRAFT,
                              verbose_name=_("Status"))
    feedback = models.TextField(blank=True, null=True, verbose_name=_("Feedback"))
    evaluated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name=_("Evaluated by"), related_name="evaluated_submissions")
    attempt_number = models.PositiveIntegerField(default=1, verbose_name=_("Attempt Number"))
    file = models.FileField(
        upload_to='submissions/%Y/%m/%d/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'jpg'])],
        verbose_name=_("Submitted File")
    )

    def calculate_score(self):
        total_score = 0
        question_scores = QuestionScore.objects.filter(exam=self.exam).select_related('question')
        manual_evaluation_needed = False
        for qs in question_scores:
            student_answer = self.answers.get(str(qs.question.id))
            if qs.question.type in [Question.QuestionTypes.MCQ, Question.QuestionTypes.TRUE_FALSE]:
                if student_answer == qs.question.correct_answer:
                    total_score += qs.score
            elif qs.question.type in [Question.QuestionTypes.ESSAY, Question.QuestionTypes.SHORT_ANSWER]:
                manual_evaluation_needed = True
        self.score = total_score
        self.status = self.SubmissionStatus.PENDING_EVALUATION if manual_evaluation_needed else self.SubmissionStatus.SUBMITTED
        self.save(update_fields=['score', 'status'])

    def is_within_time_limit(self):
        if self.exam.is_timed and self.exam.end_time:
            return self.submitted_at <= self.exam.end_time
        return True

    def remaining_attempts(self):
        if self.exam.attempt_limit == 0:
            return float('inf')
        used_attempts = Submission.objects.filter(exam=self.exam, student=self.student).count()
        return max(0, self.exam.attempt_limit - used_attempts)

    class Meta:
        unique_together = ('exam', 'student', 'attempt_number')
        indexes = [
            models.Index(fields=['student', 'submitted_at']),
            models.Index(fields=['exam', 'status']),
            models.Index(fields=['evaluated_by']),
        ]
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")

    def __str__(self):
        return f"{self.student.username} - {self.exam.subject} (Attempt {self.attempt_number})"


class ExamGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    students = models.ManyToManyField('users.User', verbose_name=_("Students"), related_name="exam_groups")
    exams = models.ManyToManyField(Exam, verbose_name=_("Exams"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    manager = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name=_("Manager"))

    class Meta:
        verbose_name = _("Exam Group")
        verbose_name_plural = _("Exam Groups")
        indexes = [models.Index(fields=['name', 'created_at'])]

    def __str__(self):
        return self.name


class ExamStatistics(models.Model):
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    average_score = models.FloatField(default=0, verbose_name=_("Average Score"))
    highest_score = models.FloatField(default=0, verbose_name=_("Highest Score"))
    lowest_score = models.FloatField(default=0, verbose_name=_("Lowest Score"))
    participants = models.PositiveIntegerField(default=0, verbose_name=_("Participants"))
    pass_rate = models.FloatField(default=0, verbose_name=_("Pass Rate (%)"))

    class Meta:
        verbose_name = _("Exam Statistics")
        verbose_name_plural = _("Exam Statistics")

    def __str__(self):
        return f"Stats for {self.exam}"


class QuestionStatistics(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Question"))
    correct_answers = models.PositiveIntegerField(default=0, verbose_name=_("Correct Answers"))
    total_attempts = models.PositiveIntegerField(default=0, verbose_name=_("Total Attempts"))
    success_rate = models.FloatField(default=0, verbose_name=_("Success Rate (%)"))

    class Meta:
        unique_together = ('exam', 'question')
        verbose_name = _("Question Statistics")
        verbose_name_plural = _("Question Statistics")

    def update_stats(self):
        submissions = Submission.objects.filter(exam=self.exam, status=Submission.SubmissionStatus.EVALUATED)
        self.total_attempts = submissions.count()
        self.correct_answers = sum(
            1 for s in submissions
            if s.answers.get(str(self.question.id)) == self.question.correct_answer
        )
        self.success_rate = (self.correct_answers / self.total_attempts * 100) if self.total_attempts > 0 else 0
        self.save()


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers',
                                   verbose_name=_("Submission"), related_query_name="answers")
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name=_("Question"), related_name="answers")
    answer_text = models.TextField(null=True, blank=True, verbose_name=_("Answer Text"))
    answer_file = models.FileField(upload_to='answers/%Y/%m/%d/', null=True, blank=True, verbose_name=_("Answer File"))

    def clean(self):
        if self.question.type == 'mcq':
            if not self.answer_text:
                raise ValidationError("MCQ requires an answer_text.")
            valid_options = [opt.option_text for opt in self.question.options.all()]
            if self.answer_text not in valid_options:
                raise ValidationError("Answer must be one of the provided options.")
        elif self.question.type == 'essay' and not (self.answer_text or self.answer_file):
            raise ValidationError("Essay requires either answer_text or answer_file.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('submission', 'question')
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return f"Answer to {self.question} by {self.submission.student}"
