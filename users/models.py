from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True, verbose_name='Пароль')
    application = models.ForeignKey(Application, default=None, on_delete=models.CASCADE)
    iin = models.CharField(max_length='12', unique=True, null=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name + " " + self.last_name + " : " + str(self.pk)


