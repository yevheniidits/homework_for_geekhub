from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.core.paginator import Paginator

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from main.models import Product
from main.forms import ProductModelForm, CreateUserForm, LoginUserForm


def register_page(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    else:
        form = CreateUserForm()
        if request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'User {user} was created')
                return redirect('start_page')
        context = {'form': form}
        return render(request, 'main/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    else:
        form = LoginUserForm()
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('start_page')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {'form': form}
    return render(request, 'main/login.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


def start_page(request):
    """All active (is_active=True) products placed in order (order_by)"""
    context = {'products': Product.objects.filter(is_active=True).order_by('-price')}
    return render(request, 'main/start_page.html', context)


def product_details(request, prod_id):
    """Detailed information about product. Make changes with product depends on action"""
    action = request.POST.get('action')
    if request.POST:
        # delete product
        if action == 'Delete':
            product = Product.objects.filter(id=prod_id)
            messages.add_message(request, messages.INFO, f'{prod_id} deleted')
            product.delete()
            return redirect(reverse('start_page'))
        # deactivate product. set product.is_active=False. still available on 'deactivated.html' page
        if action == 'Deactivate':
            product = Product.objects.filter(id=prod_id)
            messages.add_message(request, messages.INFO, f'{prod_id} deactivated')
            product.update(is_active=False)
            return redirect(reverse('details', args=(prod_id, )))
        # activate product. set product.is_active=True
        if action == 'Activate':
            product = Product.objects.filter(id=prod_id)
            product.update(is_active=True)
            messages.add_message(request, messages.INFO, f'{prod_id} activated')
            return redirect(reverse('details', args=(prod_id, )))
        # edit product. redirect to edit page
        if action == 'Edit':
            return redirect(reverse('edit', args=(prod_id, )))
        # add product to cart. quantity is 1
        if action == 'Add to cart':
            user_cart = request.session.get('cart', {})
            product = Product.objects.values().get(id=prod_id)
            product['buy_quantity'] = 1
            user_cart[str(prod_id)] = product
            request.session['cart'] = user_cart
    product = get_object_or_404(Product, pk=prod_id)
    return render(request, 'main/details.html', {'product': product})


@login_required(login_url='login')
def create_product(request):
    """Load form for creating new product"""
    if request.POST:
        # load form (forms.py) with all data from fields
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            # create and save new product
            product = form.save(commit=True)
            messages.add_message(request, messages.INFO, f'{product.title} created')
            return redirect(reverse('details', args=(product.id, )))
    return render(request, 'main/create_product.html', {'form': ProductModelForm})


@login_required(login_url='login')
def deactivated_products(request):
    """Shows all deactivated products on page"""
    context = {'products': Product.objects.filter(is_active=False)}
    return render(request, 'main/deactivated.html', context)


@login_required(login_url='login')
def edit_product(request, prod_id):
    """Get data from edit page and change product values"""
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


@login_required(login_url='login')
def cart(request):
    """Cart of products"""
    if request.POST:
        action = request.POST.get('action')
        # get cart values from session
        user_cart = request.session.get('cart', {})
        # get product from user cart
        cart_product = user_cart[request.POST['prod_id']]

        if action == 'Remove':
            del user_cart[request.POST['prod_id']]

        if action == '+':
            # check if there is enough quantity of product
            if cart_product['quantity'] < cart_product['buy_quantity'] + 1:
                messages.add_message(request, messages.INFO, 'Sorry, not enough quantity')
            else:
                cart_product['buy_quantity'] += 1

        if action == '-':
            cart_product['buy_quantity'] -= 1
            # remove product from cart if buy quantity is 0
            if cart_product['buy_quantity'] == 0:
                del user_cart[request.POST['prod_id']]

        if action == 'Add':
            # get desire number of product
            desire_quantity = int(request.POST.get('desire_quantity'))
            # check if there is enough quantity of product
            if cart_product['quantity'] < cart_product['buy_quantity'] + desire_quantity:
                messages.add_message(request, messages.INFO, 'Sorry, not enough quantity')
            else:
                cart_product['buy_quantity'] += desire_quantity

        # back to start page if cart is empty
        if not request.session['cart']:
            del request.session['cart']
            return redirect(reverse('start_page'))
        request.session['cart'] = user_cart
    return render(request, 'main/cart.html')
