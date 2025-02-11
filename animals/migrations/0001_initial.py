# Generated by Django 5.1.5 on 2025-02-10 23:18

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
            name='EntryCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100, unique=True)),
                ('total_entries', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalClassification',
            fields=[
                ('animal_classification_id', models.AutoField(primary_key=True, serialize=False)),
                ('kingdom_name', models.CharField(max_length=250)),
                ('species', models.CharField(max_length=250)),
                ('number_of_species', models.IntegerField(default=1, null=True)),
                ('animal_class', models.CharField(max_length=250)),
                ('order', models.CharField(max_length=250)),
                ('domestic', models.BooleanField(default=False)),
                ('wild_animal', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Review'), ('approved', 'Approved'), ('published', 'Published'), ('rejected', 'Rejected')], default='draft', max_length=20)),
                ('review_feedback', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('contributors', models.ManyToManyField(blank=True, related_name='contributed_animal_profiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english_name', models.CharField(max_length=250)),
                ('scientific_name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('areas_in_Uganda', models.CharField(blank=True, max_length=250, null=True)),
                ('known_values', models.TextField(blank=True, null=True)),
                ('value_details', models.TextField(blank=True, null=True)),
                ('unique_habitat', models.CharField(blank=True, max_length=250, null=True)),
                ('toxicity_to_humans', models.CharField(blank=True, max_length=250, null=True)),
                ('diet', models.CharField(blank=True, max_length=250, null=True)),
                ('behavior', models.CharField(blank=True, max_length=250, null=True)),
                ('habitat_impact', models.CharField(blank=True, max_length=250, null=True)),
                ('conservation_status', models.CharField(blank=True, max_length=250, null=True)),
                ('conservation_measures', models.CharField(blank=True, max_length=250, null=True)),
                ('reproduction', models.CharField(blank=True, max_length=250, null=True)),
                ('gestation_period', models.CharField(blank=True, max_length=250, null=True)),
                ('life_span', models.CharField(blank=True, max_length=250, null=True)),
                ('predators', models.TextField(blank=True, null=True)),
                ('prey', models.TextField(blank=True, null=True)),
                ('ethical_medicinal_uses', models.TextField(blank=True, null=True)),
                ('threats', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='animal_images')),
                ('video', models.FileField(blank=True, null=True, upload_to='animal_videos')),
                ('audio', models.FileField(blank=True, null=True, upload_to='animal_audios')),
                ('citation', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Review'), ('approved', 'Approved'), ('published', 'Published'), ('rejected', 'Rejected')], default='draft', max_length=20)),
                ('review_feedback', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('animal_classifications', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animal_profiles', to='animals.animalclassification')),
                ('contributor', models.ManyToManyField(blank=True, related_name='contributed_animals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalLocalName',
            fields=[
                ('animal_local_name_id', models.AutoField(primary_key=True, serialize=False)),
                ('local_name', models.CharField(max_length=250)),
                ('language', models.CharField(max_length=250)),
                ('contributor', models.ForeignKey(help_text='Contributor who added this local name.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='local_name_contributions', to=settings.AUTH_USER_MODEL)),
                ('animal', models.ForeignKey(help_text='The animal associated with this local name.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='local_names', to='animals.animalprofile')),
            ],
            options={
                'unique_together': {('animal', 'local_name', 'language')},
            },
        ),
    ]
