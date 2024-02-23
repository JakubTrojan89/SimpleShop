from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=64, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 're_password')

        username = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Your username',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))
        email = forms.CharField(widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))
        password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))
        re_password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
            'class': 'w-full py-4 px-6 rounded-xl'
        }))

        def clean(self):
            cleaned_data = super().clean()
            p1 = cleaned_data.get("password")
            p2 = cleaned_data.get("re_password")
            if p1 is None or p2 is None or p1 != p2:
                raise ValidationError("Passwords must be same")
            return cleaned_data

