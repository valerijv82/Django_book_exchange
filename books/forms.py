from django import forms
from .models import Comment, Book
from django.contrib.auth.models import User
from accounts.models import MyUser
from django.contrib.auth.views import PasswordChangeView


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_name', 'comment_text',)
        # exclude = ['commented_book']


class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'isbn', 'genre', 'upload', 'language',
                  'for_sale', 'price', 'for_exchange', 'for_donation']




