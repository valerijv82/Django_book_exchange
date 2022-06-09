from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from .admin import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import StarRatingsRating
from books.models import Message
from books.models import Book

User = get_user_model()
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


@login_required  # decorator limits access to logged in users.
def profile(request):
    user = request.user.id
    user_books = Book.objects.filter(owner_id=user)
    all_users_messages = Message.objects.filter(recipient=request.user.id).order_by('-timestamp')[:50]
    user_rate = 0
    rating_model = StarRatingsRating.objects.all()
    try:
        if request.user.is_authenticated:
            user_rate = rating_model.get(object_id=request.user.id)
    except:
        print("An exception occurred, possible is new and no rating yet ___________")
    instance_user = User
    form_edit_password = PasswordChangeForm(instance_user)
    context = {
        'form_edit_password': form_edit_password,
        'rate': user_rate,
        'messages': all_users_messages,
        'books': user_books
    }
    return render(request, 'registration/profile.html', context)


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Jūsų slaptažodis sėkmingai atnaujintas!')
            return render(request, 'registration/password_change_success.html')
        else:
            messages.error(request, 'Klaida, neteisingai užpildyti laukai.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    return render(request, "registration/login.html")


class PasswordChangeSuccess(TemplateView):
    template_name = 'registration/password_change_success.html'


def logout(request):
    auth.logout(request)
    return redirect('/')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/'
