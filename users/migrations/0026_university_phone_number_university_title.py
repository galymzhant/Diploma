# Generated by Django 4.2.6 on 2024-05-09 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_universityimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='university',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
