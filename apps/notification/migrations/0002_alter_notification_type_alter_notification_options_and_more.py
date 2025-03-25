# Generated by Django 5.1.7 on 2025-03-25 08:47

import ckeditor.fields
import django.utils.timezone
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notification', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('news', 'News'), ('exam', 'Exam'), ('announcement', "E'lon"), ('other', 'Other')], default='other', max_length=20, verbose_name='Type'),
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Notification', 'verbose_name_plural': 'Notifications'},
        ),
        migrations.RemoveField(
            model_name='notification',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='usernotification',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='usernotification',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='notification',
            name='cover',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=95, scale=None, size=[500, 350], upload_to='notification/%Y/%m', verbose_name='Cover'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='data',
            field=models.JSONField(blank=True, null=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='delivery_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Delivery Time'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.CharField(verbose_name='Title'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['delivery_time'], name='notificatio_deliver_832269_idx'),
        ),
        migrations.AddIndex(
            model_name='usernotification',
            index=models.Index(fields=['user', 'is_read'], name='notificatio_user_id_6562fa_idx'),
        ),
        migrations.AlterModelTable(
            name='notification',
            table=None,
        ),
        migrations.AlterModelTable(
            name='usernotification',
            table=None,
        ),
        migrations.DeleteModel(
            name='NotificationType',
        ),
    ]
