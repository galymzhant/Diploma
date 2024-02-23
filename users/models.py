from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    iin = models.CharField(max_length=12, unique=True, verbose_name='ИИН')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Application(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.user.first_name} {self.user.last_name} - {self.get_status_display()}"


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('id_card', 'Удостоверение личности'),
        ('transcript', 'Транскрипт оценок'),
        ('income_certificate', 'Справка о доходах'),
        # Add more document types as needed
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document = models.FileField(upload_to='user_documents/')
    priority_score = models.FloatField(default=0.0, verbose_name='Очки приоритета')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} of {self.user.first_name} {self.user.last_name}"


class Accommodation(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название общежития')
    total_capacity = models.PositiveIntegerField(verbose_name='Общая вместимость')
    priority_capacity = models.PositiveIntegerField(verbose_name='Вместимость для социально уязвимых')
    remaining_capacity = models.PositiveIntegerField(verbose_name='Оставшаяся вместимость')

    def __str__(self):
        return self.name


class ApplicationPriority(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='priorities')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    priority_score = models.FloatField(verbose_name='Очки приоритета')

    def __str__(self):
        return f"Priority for {self.application.user.first_name} {self.application.user.last_name} - {self.accommodation.name}"
