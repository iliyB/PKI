from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"


@login_required
def logout_user(request):
    logout(request)
    return redirect("login_url")