from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from captcha.fields import CaptchaField
#
#
User = get_user_model()


class FormWithCaptcha(forms.Form):
    mycaptcha = CaptchaField()


class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField()
    captcha = CaptchaField(label="Norėdami tęsti, įveskite paveikslėlyje matomus simbolius", required=True,)

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['email'].widget = forms.EmailInput(attrs={
    #         'placeholder': 'El. paštas',
    #         'required': True,
    #         'class': "form-email form-control"
    #         })
    #
    #     self.fields['password'].widget = forms.PasswordInput(attrs={
    #         'placeholder': 'Slaptažodis',
    #         'required': True,
    #         'class': "form-first-name form-control"
    #         })
