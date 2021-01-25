from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from main.models import Product
from main.forms import ProductModelForm


def start_page(request):
    """Выводит все продукты с заданым фильтром и сортировкой на стартовую страницу"""
    context = {'products': Product.objects.filter(is_active=True).order_by('-price')}
    return render(request, 'main/start_page.html', context)


def product_details(request, prod_id):
    """Обрабатывает действия кнопок на странице продукта и выводит соответствующее сообщение"""
    action = request.POST.get('action')
    if request.POST:
        if action == 'Delete':
            product = Product.objects.filter(id=prod_id)
            messages.add_message(request, messages.INFO, f'{prod_id} deleted')
            product.delete()
            return redirect(reverse('start_page'))
        if action == 'Deactivate':
            product = Product.objects.filter(id=prod_id)
            messages.add_message(request, messages.INFO, f'{prod_id} deactivated')
            product.update(is_active=False)
            return redirect(reverse('details', args=(prod_id, )))
        if action == 'Activate':
            product = Product.objects.filter(id=prod_id)
            product.update(is_active=True)
            messages.add_message(request, messages.INFO, f'{prod_id} activated')
            return redirect(reverse('details', args=(prod_id, )))
        if action == 'Edit':
            return redirect(reverse('edit', args=(prod_id, )))
    product = get_object_or_404(Product, pk=prod_id)
    return render(request, 'main/details.html', {'product': product})


def create_product(request):
    """Загружает форму для создания нового продукта и выводит сообщение при успешном создании"""
    if request.POST:
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=True)
            messages.add_message(request, messages.INFO, f'{product.title} created')
            return redirect(reverse('details', args=(product.id, )))
    return render(request, 'main/create_product.html', {'form': ProductModelForm})


def deactivated_products(request):
    """Выводит деактивированые продукты в виде ссылок на страницы продуктов"""
    context = {'products': Product.objects.filter(is_active=False)}
    return render(request, 'main/deactivated.html', context)


def edit_product(request, prod_id):
    """Обрабатывает данные с полей на странице редактирования продукта и выводит подтверждающее сообщение"""
    product = Product.objects.get(id=prod_id)
    if request.POST:
        product.title = request.POST.get("title")
        product.old_price = request.POST.get("old_price")
        product.price = request.POST.get("price")
        product.quantity = request.POST.get("quantity")
        product.description = request.POST.get("description")
        product.save()
        messages.add_message(request, messages.INFO, f'{product.title} updated')
        return redirect(reverse('details', args=(prod_id,)))
    return render(request, 'main/edit.html', {'product': product})

# Create your views here.
