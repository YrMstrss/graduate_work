from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    birthday = models.DateField(verbose_name='дата рождения', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    phone = models.CharField(unique=True, max_length=100, verbose_name='номер телефона')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    username = models.CharField(unique=True, max_length=100)

    token = models.CharField(max_length=4, default=None, verbose_name='токен', **NULLABLE)

    subscriptions = models.ManyToManyField('User', verbose_name='подписки', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:

        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
