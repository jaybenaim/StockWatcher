# Generated by Django 3.2.3 on 2021-10-10 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mainApp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0003_rename_watcher_tickerwatcher_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('as_url', models.TextField(blank=True, max_length=500, null=True)),
                ('as_file', models.ImageField(blank=True, null=True, upload_to=mainApp.models.make_unique_picture_filename)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=30, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('avatar_url', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainApp.image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
