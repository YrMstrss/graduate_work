from django.db import models


class Publication(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержание')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
