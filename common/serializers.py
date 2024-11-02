from rest_framework import serializers

from common.models import Subjects, Examine, Assignment, Submission, ExamResult
from users.models import User


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['title', 'description']


class ExamineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examine
        fields = ['subjects', 'exam_name', 'start_time', 'end_time', 'question_count', 'passing_percentage',
                  'total_score', 'active', 'assigned_users']


class AssignStudentsSerializer(serializers.Serializer):
    # assigned_users maydoni olib tashlandi
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True  # Agar bu maydon yozish uchun kerak bo'lsa
    )

    def create(self, validated_data):
        assigned_users = validated_data.pop('assigned_users')
        exam = self.context['exam']
        assignments = []

        for user in assigned_users:
            # Assignment obyektini yaratish
            assignment = Assignment(student=user, exam=exam)
            assignments.append(assignment)

        Assignment.objects.bulk_create(assignments)
        return validated_data


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField(max_length=100)


class TestSubmissionSerializer(serializers.Serializer):
    answers = serializers.ListSerializer(
        child=SubmitAnswerSerializer(),
        help_text="Savollar ro'yxati va javoblar."
    )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['exam', 'question', 'answer']


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = ['id', 'student', 'exam', 'score', 'passed']
