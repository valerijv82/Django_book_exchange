import captcha
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .admin import UserCreationForm
from .forms import LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import StarRatingsRating

User = get_user_model()


@login_required  # decorator limits access to logged in users.
def profile(request):
    user_rate = None
    rating_model = StarRatingsRating.objects.all()
    try:
        if request.user.is_authenticated:
            user_rate = rating_model.get(object_id=request.user.id)
    except:
        print("An exception occurred")
    instance_user = User
    form_edit_password = PasswordChangeForm(instance_user)
    context = {
        'form_edit_password': form_edit_password,
        'rate': user_rate
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
            messages.error(request, 'Ištaisykite toliau pateiktą klaidą.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print(captcha.get_version())
                return redirect("/")
            else:
                request.session['invalid_user'] = 1
    form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


class PasswordChangeSuccess(TemplateView):
    template_name = 'registration/password_change_success.html'


def logout(request):
    auth.logout(request)
    return redirect('/')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/'


class LoginView(CreateView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = '/'
