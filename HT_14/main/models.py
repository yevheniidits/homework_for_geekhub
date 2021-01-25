from django.db import models


class Product(models.Model):
    """Содержит атрибуты/параметры для любого продукта/товара"""
    title = models.CharField(max_length=50, verbose_name='Название', default='Untitled product')
    old_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Старая цена',
                                    default=0, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена', default=0)
    image = models.ImageField(upload_to='main/static/images', default=f'{title}.jpg',
                              verbose_name='Изображение', blank=True)
    description = models.TextField(verbose_name='Описание товара', default='No description', blank=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    is_active = models.BooleanField(verbose_name='В продаже', default=False)

    def __str__(self):
        return f'{self.id}: {self.title}'











# Create your models here.
