# Generated by Django 4.2.6 on 2024-03-24 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_is_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCreateRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('email', models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')),
                ('username', models.CharField(max_length=255, null=True, unique=True)),
                ('password', models.CharField(max_length=255, null=True, verbose_name='Пароль')),
                ('sms_code', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
