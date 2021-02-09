from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from main.models import Product


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):

    class Meta:
        model = User
        fields = '__all__'




