from django.contrib.auth import views as auth_views
from django.urls import path
from accounts.views import (RegisterView,
                            profile,
                            password_change,
                            logout,
                            login_user
                            )

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/password_change/', password_change, name='change_password'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
