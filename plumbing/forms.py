from django import forms
from .models import User, Comments, Order


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'phone_number', )
