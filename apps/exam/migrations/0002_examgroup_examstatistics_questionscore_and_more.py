# Generated by Django 5.1.7 on 2025-03-25 06:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': 'Exam', 'verbose_name_plural': 'Exams'},
        ),
        migrations.AlterModelOptions(
            name='submission',
            options={'verbose_name': 'Submission', 'verbose_name_plural': 'Submissions'},
        ),
        migrations.RemoveField(
            model_name='exam',
            name='end_time',
        ),
        migrations.AddField(
            model_name='exam',
            name='attempt_limit',
            field=models.PositiveIntegerField(default=1, verbose_name='Attempt Limit'),
        ),
        migrations.AddField(
            model_name='exam',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Is Published'),
        ),
        migrations.AddField(
            model_name='exam',
            name='is_timed',
            field=models.BooleanField(default=True, verbose_name='Is Timed'),
        ),
        migrations.AddField(
            model_name='exam',
            name='randomize_questions',
            field=models.BooleanField(default=False, verbose_name='Randomize Questions'),
        ),
        migrations.AddField(
            model_name='submission',
            name='answers',
            field=models.JSONField(default=1, verbose_name='Answers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='attempt_number',
            field=models.PositiveIntegerField(default=1, verbose_name='Attempt Number'),
        ),
        migrations.AddField(
            model_name='submission',
            name='evaluated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evaluated_submissions', to=settings.AUTH_USER_MODEL, verbose_name='Evaluated by'),
        ),
        migrations.AddField(
            model_name='submission',
            name='feedback',
            field=models.TextField(blank=True, null=True, verbose_name='Feedback'),
        ),
        migrations.AddField(
            model_name='submission',
            name='finished_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Finished At'),
        ),
        migrations.AddField(
            model_name='submission',
            name='score',
            field=models.FloatField(blank=True, null=True, verbose_name='Score'),
        ),
        migrations.AddField(
            model_name='submission',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Started At'),
        ),
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('evaluated', 'Evaluated')], default='draft', max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='duration',
            field=models.PositiveIntegerField(verbose_name='Duration (minutes)'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='max_score',
            field=models.PositiveIntegerField(default=100, verbose_name='Max Score'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('draft', 'Draft'), ('finished', 'Finished')], default='draft', max_length=10, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Correct Answer'),
        ),
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.JSONField(blank=True, null=True, verbose_name='Options'),
        ),
        migrations.AlterUniqueTogether(
            name='submission',
            unique_together={('exam', 'student', 'attempt_number')},
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(fields=['student', 'submitted_at'], name='exam_submis_student_103fd9_idx'),
        ),
        migrations.AddField(
            model_name='examgroup',
            name='exams',
            field=models.ManyToManyField(to='exam.exam', verbose_name='Exams'),
        ),
        migrations.AddField(
            model_name='examgroup',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Students'),
        ),
        migrations.AddField(
            model_name='examstatistics',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.exam', verbose_name='Exam'),
        ),
        migrations.AddField(
            model_name='questionscore',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.exam', verbose_name='Exam'),
        ),
        migrations.AddField(
            model_name='questionscore',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.question', verbose_name='Question'),
        ),
        migrations.AlterUniqueTogether(
            name='questionscore',
            unique_together={('exam', 'question')},
        ),
    ]
