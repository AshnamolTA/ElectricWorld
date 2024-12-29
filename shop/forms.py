from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django import forms

from shop.models import UserProfile,Order


class SignUpForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","password1","password2"]

class SignInForm(forms.Form):

    username=forms.CharField()

    password=forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):

    class Meta:

        model=UserProfile

        fields=["bio","profile_picture","phone"]

class OrderForm(forms.ModelForm):

    class Meta:

        model=Order

        fields=["name","delivery_address","phone","email","pincode","city","state","payment_mode"]