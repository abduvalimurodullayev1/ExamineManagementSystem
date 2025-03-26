# Generated by Django 5.1.7 on 2025-03-26 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_verification_code_user_verification_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_token',
            field=models.CharField(blank=True, help_text='6-digit code for email verification', max_length=120, verbose_name='Verification Code'),
        ),
    ]
