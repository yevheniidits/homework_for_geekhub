from django.contrib import admin
from main.models import Product, SubCategory, Category


class AdminProduct(admin.ModelAdmin):
    list_display_links = ['title']
    list_display = ['title', 'sub_category', 'get_category', 'price', 'is_active']
    list_filter = ['sub_category', 'is_active']
    actions = ['activate_product', 'deactivate_product']

    @staticmethod
    def activate_product(self, request, queryset):
        queryset.update(is_active=True)

    @staticmethod
    def deactivate_product(self, request, queryset):
        queryset.update(is_active=False)

    def get_category(self, product):
        return product.sub_category.category.name

    get_category.short_description = 'Категория'


admin.site.register(Product, AdminProduct)
admin.site.register(SubCategory)
admin.site.register(Category)


# Register your models here.
