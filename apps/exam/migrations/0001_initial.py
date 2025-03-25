# Generated by Django 5.1.7 on 2025-03-25 10:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.CharField(choices=[('mcq', 'Multiple Choice'), ('essay', 'Essay'), ('mixed', 'Mixed')], default='mcq', max_length=20, verbose_name='Exam Type')),
                ('status', models.CharField(choices=[('active', 'Active'), ('draft', 'Draft'), ('finished', 'Finished')], default='draft', max_length=10, verbose_name='Status')),
                ('duration', models.PositiveIntegerField(verbose_name='Duration (minutes)')),
                ('start_time', models.DateTimeField(verbose_name='Start time')),
                ('max_score', models.PositiveIntegerField(default=100, verbose_name='Max Score')),
                ('attempt_limit', models.PositiveIntegerField(default=1, verbose_name='Attempt Limit')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is Published')),
                ('is_timed', models.BooleanField(default=True, verbose_name='Is Timed')),
                ('randomize_questions', models.BooleanField(default=False, verbose_name='Randomize Questions')),
            ],
            options={
                'verbose_name': 'Exam',
                'verbose_name_plural': 'Exams',
            },
        ),
        migrations.CreateModel(
            name='ExamGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'ExamGroup',
                'verbose_name_plural': 'ExamGroups',
            },
        ),
        migrations.CreateModel(
            name='ExamStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_score', models.FloatField(verbose_name='Average Score')),
                ('highest_score', models.FloatField(verbose_name='Highest Score')),
                ('lowest_score', models.FloatField(verbose_name='Lowest Score')),
                ('participants', models.PositiveIntegerField(verbose_name='Participants')),
            ],
            options={
                'verbose_name': 'Exam Statistics',
                'verbose_name_plural': 'Exam Statistics',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='Question Body')),
                ('correct_answer', models.CharField(blank=True, max_length=100, null=True, verbose_name='Correct Answer')),
                ('options', models.JSONField(blank=True, null=True, verbose_name='Options')),
                ('type', models.CharField(default='Multiple Choice', max_length=50, verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='QuestionScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=1, verbose_name='Score')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Question Score',
                'verbose_name_plural': 'Question Scores',
            },
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=122, verbose_name='Title')),
                ('description', models.TextField(max_length=500, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(blank=True, null=True, verbose_name='Started At')),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Submitted At')),
                ('finished_at', models.DateTimeField(blank=True, null=True, verbose_name='Finished At')),
                ('answers', models.JSONField(verbose_name='Answers')),
                ('score', models.FloatField(blank=True, null=True, verbose_name='Score')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('evaluated', 'Evaluated')], default='draft', max_length=20, verbose_name='Status')),
                ('feedback', models.TextField(blank=True, null=True, verbose_name='Feedback')),
                ('attempt_number', models.PositiveIntegerField(default=1, verbose_name='Attempt Number')),
                ('file', models.FileField(blank=True, null=True, upload_to='submissions/%Y/%m/%d/', verbose_name='Submitted File')),
            ],
            options={
                'verbose_name': 'Submission',
                'verbose_name_plural': 'Submissions',
            },
        ),
    ]
