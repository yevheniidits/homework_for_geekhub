from django.db import models


class ScrapedOlxAd(models.Model):
    url = models.URLField(verbose_name='Обьявление')
    title = models.CharField(verbose_name='Название', max_length=255, default='Без названия', blank=True)
    text = models.TextField(verbose_name='Текст обьявления', null=True, blank=True)
    author_name = models.CharField(verbose_name='Имя автора', max_length=50, default='Неизвестный', blank=True)
    author_phone_number = models.CharField(verbose_name='Номер телефона', max_length=100, default='Неизвестно', blank=True)
    author_info = models.CharField(verbose_name='Об авторе', max_length=255, default='Неизвестно', blank=True)

    def __str__(self):
        return f'{self.title} | {self.author_name}'
