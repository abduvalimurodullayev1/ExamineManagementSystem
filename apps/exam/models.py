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

    class ExamTypes(models.TextChoices):
        MCQ = "mcq", _("Multiple Choice")
        ESSAY = "essay", _("Essay")
        MIXED = "mixed", _("Mixed")

    exam_type = models.CharField(max_length=20, choices=ExamTypes, default=ExamTypes.MCQ, verbose_name=_("Exam Type"))
    status = models.CharField(max_length=10, choices=ExamStatus.choices, default=ExamStatus.DRAFT,
                              verbose_name=_("Status"))
    duration = models.PositiveIntegerField(verbose_name=_("Duration (minutes)"))
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    start_time = models.DateTimeField(verbose_name=_("Start time"))
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_("Created by"))
    max_score = models.PositiveIntegerField(verbose_name=_("Max Score"), default=100)
    questions = models.ManyToManyField("Question", verbose_name=_("Questions"), blank=True)
    attempt_limit = models.PositiveIntegerField(default=1, verbose_name=_("Attempt Limit"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is Published"))
    is_timed = models.BooleanField(default=True, verbose_name=_("Is Timed"))
    randomize_questions = models.BooleanField(default=False, verbose_name=_("Randomize Questions"))

    def clean(self):
        if self.duration <= 0:
            raise ValidationError(_("Duration cannot be negative or zero."))
        if self.start_time < timezone.now():
            raise ValidationError(_("Start time cannot be in the past."))
        if self.questions.exists():
            total_question_score = sum(qs.score for qs in QuestionScore.objects.filter(exam=self))
            if total_question_score != self.max_score:
                raise ValidationError(_("Total score of questions must match max_score."))

    @property
    def end_time(self):
        from datetime import timedelta
        return self.start_time + timedelta(minutes=self.duration) if self.is_timed else None

    def get_statistics(self):
        submissions = Submission.objects.filter(exam=self, status="evaluated")
        if not submissions.exists():
            return {"average_score": 0, "highest_score": 0, "lowest_score": 0, "participants": 0}
        scores = [s.score for s in submissions if s.score is not None]
        return {
            "average_score": sum(scores) / len(scores) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "participants": submissions.count(),
        }

    class Meta:
        indexes = [models.Index(fields=['start_time', 'status'])]
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")

    def __str__(self):
        return f"{self.subject.title} - {self.start_time}"


class Question(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, verbose_name=_("Subject"))
    body = models.TextField(verbose_name=_("Question Body"))
    correct_answer = models.CharField(verbose_name=_("Correct Answer"), max_length=100, blank=True, null=True)
    options = models.JSONField(verbose_name=_("Options"), blank=True, null=True)
    type = models.CharField(max_length=50, verbose_name=_("Type"), default="Multiple Choice")

    def clean(self):
        if self.type == "Multiple Choice" and (not self.options or not self.correct_answer):
            raise ValidationError(_("Multiple Choice questions must have options and a correct answer."))
        if self.type == "Essay" and (self.options or self.correct_answer):
            raise ValidationError(_("Essay questions should not have options or a correct answer."))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.body


class QuestionScore(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("Question"))
    score = models.PositiveIntegerField(verbose_name=_("Score"), default=1)
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        unique_together = ('question', 'exam')
        verbose_name = _("Question Score")
        verbose_name_plural = _("Question Scores")


class Submission(models.Model):
    class SubmissionStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SUBMITTED = "submitted", _("Submitted")
        EVALUATED = "evaluated", _("Evaluated")

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    student = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("Student"))
    started_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Started At"))
    submitted_at = models.DateTimeField(default=timezone.now, verbose_name=_("Submitted At"), )
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Finished At"))
    answers = models.JSONField(verbose_name=_("Answers"))
    score = models.FloatField(verbose_name=_("Score"), null=True, blank=True)
    status = models.CharField(max_length=20, choices=SubmissionStatus.choices, default=SubmissionStatus.DRAFT, verbose_name=_("Status"))
    feedback = models.TextField(blank=True, null=True, verbose_name=_("Feedback"))
    evaluated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Evaluated by"), related_name="evaluated_submissions")
    attempt_number = models.PositiveIntegerField(default=1, verbose_name=_("Attempt Number"))
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True, blank=True, verbose_name=_("Submitted File"))

    def calculate_score(self):
        total_score = 0
        question_scores = QuestionScore.objects.filter(exam=self.exam)
        if not question_scores.exists():
            self.score = 0
        else:
            for qs in question_scores:
                if qs.question.type == "Multiple Choice":
                    student_answer = self.answers.get(str(qs.question.id))
                    if student_answer == qs.question.correct_answer:
                        total_score += qs.score
            self.score = total_score
        self.status = self.SubmissionStatus.SUBMITTED
        self.save()

    class Meta:
        unique_together = ('exam', 'student', 'attempt_number')
        indexes = [models.Index(fields=['student', 'submitted_at'])]
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")

    def __str__(self):
        return f"{self.student.username} - {self.exam.subject} (Attempt {self.attempt_number})"

class ExamGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    students = models.ManyToManyField('users.User', verbose_name=_("Students"))
    exams = models.ManyToManyField(Exam, verbose_name=_("Exams"))

    class Meta:
        verbose_name = _("ExamGroup")
        verbose_name_plural = _("ExamGroups")

    def __str__(self):
        return self.name


class ExamStatistics(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_("Exam"))
    average_score = models.FloatField(verbose_name=_("Average Score"))
    highest_score = models.FloatField(verbose_name=_("Highest Score"))
    lowest_score = models.FloatField(verbose_name=_("Lowest Score"))
    participants = models.PositiveIntegerField(verbose_name=_("Participants"))

    class Meta:
        verbose_name = _("Exam Statistics")
        verbose_name_plural = _("Exam Statistics")
