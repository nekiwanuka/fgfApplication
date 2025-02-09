# Generated by Django 5.1.5 on 2025-02-08 20:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='animalprofile',
            old_name='date_entered',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='animalclassification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='animalclassification',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='animalclassification',
            name='review_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='animalclassification',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Review'), ('approved', 'Approved'), ('published', 'Published'), ('rejected', 'Rejected')], default='draft', max_length=20),
        ),
        migrations.AddField(
            model_name='animalclassification',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='animalprofile',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='animalprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='animallocalname',
            name='contributor',
            field=models.ForeignKey(help_text='Contributor who added this local name.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='local_name_contributions', to=settings.AUTH_USER_MODEL),
        ),
    ]
