from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from captcha.fields import CaptchaField
#
#
User = get_user_model()
#
#


class LoginForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    captcha = CaptchaField( label="What does this say?", required=True,)

#
#
# class RegisterForm(forms.ModelForm):
#     username = forms.CharField(label='Username')
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#     captcha = CaptchaField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError("Username is taken")
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("Email is taken")
#         return email
#
#     def clean_password(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password2 = cleaned_data.get("password")
#         if password2 is not None and password != password2:
#             self.add_error("password2", "Your passwords must match")
#         return password
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserAdminCreationForm(forms.ModelForm):
#     """
#     A form for creating new users. Includes all the required
#     fields, plus a repeated password.
#     """
#     password = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ['email']
#
#     def clean(self):
#         '''
#         Verify both passwords match.
#         '''
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password2 = cleaned_data.get("password")
#         if password2 is not None and password != password2:
#             self.add_error("password2", "Your passwords must match")
#         return cleaned_data
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserAdminChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'is_active', 'admin']
#
#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]
