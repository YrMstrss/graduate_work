from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}

TYPE_CHOICES = [
    ('for_all', 'доступна всем пользователям'),
    ('for_reg', 'доступна зарегистрированным пользователям'),
    ('for_sub', 'доступна пользователям с оплаченной подпиской'),
]


class Publication(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержание')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор публикации', **NULLABLE)

    publication_type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='for_all',
                                        verbose_name='тип публикации')
    views = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Likes(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, verbose_name='запись')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='кто лайкнул')
    is_active = models.BooleanField(default=False, verbose_name='лайк')

    def __str__(self):
        return f'Лайк для публикации {self.publication} от {self.user}'

    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'


class Dislikes(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, verbose_name='запись')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='кто дизлайкнул')
    is_active = models.BooleanField(default=False, verbose_name='дизлайк')

    def __str__(self):
        return f'Дизлайк для публикации {self.publication} от {self.user}'

    class Meta:
        verbose_name = 'дизлайк'
        verbose_name_plural = 'дизлайки'
