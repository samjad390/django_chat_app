from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class MyLoginView(LoginView):
    """
    Custom LoginView that renders the 'users/login.html' template.
    """
    template_name = 'users/login.html'


class RegisterView(CreateView):
    """
    CreateView that uses UserCreationForm as the form class, redirects to 'login' on successful form submission.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'
