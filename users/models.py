from xml.dom.minidom import Document

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Partner(models.Model):
    name = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    document_url = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    available_places = models.IntegerField()
    image = models.ImageField(upload_to='', blank=True, null=True, default=None)
    address = models.CharField(max_length=255, blank=True)
    distance = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    price = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name

class UniversityImage(models.Model):
    post = models.ForeignKey(University, default=None, on_delete=models.CASCADE)
    images = models.ImageField()

    def __str__(self):
        return self.post.name


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    iin = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True, verbose_name='Пароль')
    user_documents = models.ManyToManyField('Document', blank=True, default=[], verbose_name='Документы')
    apply_approved = models.BooleanField(default=False, verbose_name='')
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name='Универ', default=None, null=True)
    created_date = models.DateField(blank=True, null=True)
    place = models.CharField(max_length=255, verbose_name='Место в общаге', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def toJson(self):
        return {
            'id': self.id,
            'name': self.first_name,
            'surname': self.last_name,
            'iin': self.iin,
            'phone': self.phone_number,
            'birth_date': self.birth_date,
            'email': self.email
        };

    # USERNAME_FIELD = phone_number

    def __str__(self):
        return self.first_name + " " + self.last_name + " : " + str(self.pk)


class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.text


class UserCreateRequest(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True, verbose_name='Пароль')
    sms_code = models.CharField(max_length=6, blank=True, null=True)
    iin = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Запрос на регистрацию'
        verbose_name_plural = 'Запросы на регистрацию'

    # USERNAME_FIELD = phone_number

    def __str__(self):
        return self.first_name + " " + self.last_name + " : " + str(self.pk)


class Type(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название документа')
    score = models.IntegerField(default=0, help_text="Score based on the document's importance.")
    required = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class Document(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]
    decline_reason = models.CharField(max_length=255, default='', null=True, blank=True)
    title = models.ForeignKey(Type, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    file = models.FileField(blank=True, null=True)
    def __str__(self):
        return f'{self.title} - {self.status}'
