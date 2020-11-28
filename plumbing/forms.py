from django import forms

from .models import User, Comments, Order
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'phone_number',)
