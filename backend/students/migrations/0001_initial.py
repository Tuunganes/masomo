# Generated by Django 5.1.5 on 2025-05-30 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('date_of_birth', models.DateField()),
                ('nationality', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('guardian_name', models.CharField(blank=True, max_length=120)),
                ('guardian_phone', models.CharField(blank=True, max_length=30)),
                ('class_level', models.CharField(blank=True, max_length=50)),
                ('enrol_date', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('alumni', 'Alumni'), ('transferred', 'Transferred')], default='active', max_length=12)),
                ('photo', models.ImageField(blank=True, upload_to='student_photos/')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
