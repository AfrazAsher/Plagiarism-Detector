# Generated by Django 3.2.15 on 2024-06-24 23:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academic', '0005_alter_userprofile_full_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='deadline',
            new_name='due_date',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='content',
        ),
        migrations.AddField(
            model_name='assignment',
            name='attachments',
            field=models.FileField(blank=True, upload_to='attachments/'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='description',
            field=models.TextField(default='No description provided'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='file_upload_instructions',
            field=models.TextField(blank=True, default='No specific instructions'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='grading_criteria',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='max_marks',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='assignment',
            name='submission_format',
            field=models.CharField(default='PDF', max_length=50),
        ),
        migrations.AddField(
            model_name='course',
            name='course_code',
            field=models.CharField(default='UNKNOWN', max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='credits',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(default='No description provided'),
        ),
        migrations.AddField(
            model_name='course',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 24, 23, 5, 36, 794318)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.CharField(default='Unknown Instructor', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 24, 23, 7, 7, 420341)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='academic.course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
