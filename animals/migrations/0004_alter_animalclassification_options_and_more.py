# Generated by Django 5.1.5 on 2025-02-11 01:37

import animals.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0003_remove_animalprofile_animal_classifications_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animalclassification',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='animallocalname',
            options={'ordering': ['local_name']},
        ),
        migrations.AlterModelOptions(
            name='animalprofile',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='entrycounter',
            options={'ordering': ['model_name']},
        ),
        migrations.AlterField(
            model_name='animalclassification',
            name='animal_class',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animalclassification',
            name='kingdom_name',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animalclassification',
            name='order',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animalclassification',
            name='species',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animallocalname',
            name='language',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animallocalname',
            name='local_name',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animalprofile',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to=animals.models.animal_media_upload_path),
        ),
        migrations.RemoveField(
            model_name='animalprofile',
            name='contributor',
        ),
        migrations.AlterField(
            model_name='animalprofile',
            name='english_name',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animalprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=animals.models.animal_media_upload_path),
        ),
        migrations.AlterField(
            model_name='animalprofile',
            name='scientific_name',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='animalprofile',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=animals.models.animal_media_upload_path),
        ),
        migrations.AddField(
            model_name='animalprofile',
            name='contributor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animal_profile_contributions', to=settings.AUTH_USER_MODEL),
        ),
    ]
