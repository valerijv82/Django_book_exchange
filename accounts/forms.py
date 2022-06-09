from django import forms
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
User = get_user_model()


class FormWithCaptcha(forms.Form):
    mycaptcha = CaptchaField()


class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField()
    captcha = CaptchaField(required=True)

