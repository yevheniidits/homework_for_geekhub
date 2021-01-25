from django import forms

from main.models import Product


class ProductModelForm(forms.ModelForm):
    """Форма содержащая все поля (атрибуты) продукта.
       Используется для создания нового продукта
    """
    class Meta:
        model = Product
        fields = '__all__'
