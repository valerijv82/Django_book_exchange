from django import forms
from .models import Comment, Book, Message


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_name', 'comment_text',)


class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'isbn', 'genre', 'upload', 'language',
                  'for_sale', 'price', 'for_exchange', 'for_donation']


class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)


