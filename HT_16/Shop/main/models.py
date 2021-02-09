from django.db import models


class Product(models.Model):
    """Main class for product"""
    title = models.CharField(max_length=50, verbose_name='Название', default='Untitled product')
    sub_category = models.ForeignKey('main.SubCategory', verbose_name='Подкатегория', on_delete=models.CASCADE, blank=True, null=True)
    old_price = models.PositiveIntegerField(verbose_name='Старая цена', default=0, blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='Цена', default=0)
    image = models.ImageField(upload_to='main/static/images/', default=f'{title}.jpg',
                              verbose_name='Изображение', blank=True)
    description = models.TextField(verbose_name='Описание товара', default='No description', blank=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    is_active = models.BooleanField(verbose_name='В продаже', default=False)

    def __str__(self):
        return f'{self.id}: {self.title}'


class SubCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Подкатегория', default='Other')
    category = models.ForeignKey('main.Category', verbose_name='Категория', on_delete=models.CASCADE, default='Other')

    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория', default='New unnamed category')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Категория {self.name}'

# Create your models here.
