# Generated by Django 3.2.3 on 2021-09-29 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticker',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='tickerwatcher',
            options={'ordering': ['-updated_at']},
        ),
    ]
