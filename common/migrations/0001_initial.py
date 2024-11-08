# Generated by Django 5.1.2 on 2024-11-02 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='Question Body')),
                ('body_uz', models.TextField(null=True, verbose_name='Question Body')),
                ('body_ru', models.TextField(null=True, verbose_name='Question Body')),
                ('body_en', models.TextField(null=True, verbose_name='Question Body')),
                ('body_de', models.TextField(null=True, verbose_name='Question Body')),
                ('correct_answer', models.CharField(max_length=100, verbose_name='Correct Answer')),
                ('correct_answer_uz', models.CharField(max_length=100, null=True, verbose_name='Correct Answer')),
                ('correct_answer_ru', models.CharField(max_length=100, null=True, verbose_name='Correct Answer')),
                ('correct_answer_en', models.CharField(max_length=100, null=True, verbose_name='Correct Answer')),
                ('correct_answer_de', models.CharField(max_length=100, null=True, verbose_name='Correct Answer')),
                ('options', models.JSONField(verbose_name='Options')),
                ('options_uz', models.JSONField(null=True, verbose_name='Options')),
                ('options_ru', models.JSONField(null=True, verbose_name='Options')),
                ('options_en', models.JSONField(null=True, verbose_name='Options')),
                ('options_de', models.JSONField(null=True, verbose_name='Options')),
                ('type', models.CharField(default='Multiple Choice', max_length=50, verbose_name='Type')),
                ('type_uz', models.CharField(default='Multiple Choice', max_length=50, null=True, verbose_name='Type')),
                ('type_ru', models.CharField(default='Multiple Choice', max_length=50, null=True, verbose_name='Type')),
                ('type_en', models.CharField(default='Multiple Choice', max_length=50, null=True, verbose_name='Type')),
                ('type_de', models.CharField(default='Multiple Choice', max_length=50, null=True, verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=122, verbose_name='Title')),
                ('title_uz', models.CharField(max_length=122, null=True, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=122, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=122, null=True, verbose_name='Title')),
                ('title_de', models.CharField(max_length=122, null=True, verbose_name='Title')),
                ('description', models.TextField(max_length=500, verbose_name='Description')),
                ('description_uz', models.TextField(max_length=500, null=True, verbose_name='Description')),
                ('description_ru', models.TextField(max_length=500, null=True, verbose_name='Description')),
                ('description_en', models.TextField(max_length=500, null=True, verbose_name='Description')),
                ('description_de', models.TextField(max_length=500, null=True, verbose_name='Description')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('active_uz', models.BooleanField(default=True, verbose_name='Active')),
                ('active_ru', models.BooleanField(default=True, verbose_name='Active')),
                ('active_en', models.BooleanField(default=True, verbose_name='Active')),
                ('active_de', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='Examine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=100, verbose_name='Exam name')),
                ('exam_name_uz', models.CharField(max_length=100, null=True, verbose_name='Exam name')),
                ('exam_name_ru', models.CharField(max_length=100, null=True, verbose_name='Exam name')),
                ('exam_name_en', models.CharField(max_length=100, null=True, verbose_name='Exam name')),
                ('exam_name_de', models.CharField(max_length=100, null=True, verbose_name='Exam name')),
                ('start_time', models.DateTimeField(verbose_name='Start time')),
                ('end_time', models.DateTimeField(verbose_name='End time')),
                ('question_count', models.PositiveIntegerField(verbose_name='Question count')),
                ('passing_percentage', models.PositiveIntegerField(default=50, verbose_name='Passing percentage')),
                ('total_score', models.PositiveIntegerField(verbose_name='Total score')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('active_uz', models.BooleanField(default=True, verbose_name='Active')),
                ('active_ru', models.BooleanField(default=True, verbose_name='Active')),
                ('active_en', models.BooleanField(default=True, verbose_name='Active')),
                ('active_de', models.BooleanField(default=True, verbose_name='Active')),
                ('assigned_users', models.ManyToManyField(blank=True, related_name='assigned_exams', to=settings.AUTH_USER_MODEL, verbose_name='Assigned users')),
                ('questions', models.ManyToManyField(blank=True, related_name='exams', to='common.question', verbose_name='Questions')),
                ('subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.subjects', verbose_name='Subject')),
            ],
            options={
                'verbose_name': 'Examine',
                'verbose_name_plural': 'Examines',
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('assigned_at', models.DateTimeField(auto_now_add=True, verbose_name='Assigned at')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('completed_uz', models.BooleanField(default=False, verbose_name='Completed')),
                ('completed_ru', models.BooleanField(default=False, verbose_name='Completed')),
                ('completed_en', models.BooleanField(default=False, verbose_name='Completed')),
                ('completed_de', models.BooleanField(default=False, verbose_name='Completed')),
                ('completion_date', models.DateTimeField(blank=True, null=True, verbose_name='Completion Date')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='common.examine', verbose_name='Exam')),
            ],
            options={
                'verbose_name': 'Assignment',
                'verbose_name_plural': 'Assignments',
            },
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(verbose_name='Score')),
                ('score_uz', models.PositiveIntegerField(null=True, verbose_name='Score')),
                ('score_ru', models.PositiveIntegerField(null=True, verbose_name='Score')),
                ('score_en', models.PositiveIntegerField(null=True, verbose_name='Score')),
                ('score_de', models.PositiveIntegerField(null=True, verbose_name='Score')),
                ('passed', models.BooleanField(default=False, verbose_name='Passed')),
                ('passed_uz', models.BooleanField(default=False, verbose_name='Passed')),
                ('passed_ru', models.BooleanField(default=False, verbose_name='Passed')),
                ('passed_en', models.BooleanField(default=False, verbose_name='Passed')),
                ('passed_de', models.BooleanField(default=False, verbose_name='Passed')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.examine', verbose_name='Exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name': 'ExamResult',
                'verbose_name_plural': 'ExamResults',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('message', models.TextField(verbose_name='Message')),
                ('message_uz', models.TextField(null=True, verbose_name='Message')),
                ('message_ru', models.TextField(null=True, verbose_name='Message')),
                ('message_en', models.TextField(null=True, verbose_name='Message')),
                ('message_de', models.TextField(null=True, verbose_name='Message')),
                ('is_read', models.BooleanField(default=False, verbose_name='Is Read')),
                ('is_read_uz', models.BooleanField(default=False, verbose_name='Is Read')),
                ('is_read_ru', models.BooleanField(default=False, verbose_name='Is Read')),
                ('is_read_en', models.BooleanField(default=False, verbose_name='Is Read')),
                ('is_read_de', models.BooleanField(default=False, verbose_name='Is Read')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Is Sent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.subjects', verbose_name='Subject'),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=100, verbose_name='Answer')),
                ('answer_uz', models.CharField(max_length=100, null=True, verbose_name='Answer')),
                ('answer_ru', models.CharField(max_length=100, null=True, verbose_name='Answer')),
                ('answer_en', models.CharField(max_length=100, null=True, verbose_name='Answer')),
                ('answer_de', models.CharField(max_length=100, null=True, verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is correct')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.examine', verbose_name='Exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.question', verbose_name='Question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Submission',
                'verbose_name_plural': 'Submissions',
            },
        ),
    ]
