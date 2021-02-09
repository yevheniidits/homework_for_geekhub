from django.urls import path

from main import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('create/', views.create_product, name='create'),
    path('deactivated/', views.deactivated_products, name='deactivated'),
    path('<int:prod_id>/', views.product_details, name='details'),
    path('<int:prod_id>/edit/', views.edit_product, name='edit'),
]
