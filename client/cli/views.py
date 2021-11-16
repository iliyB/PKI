from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from .models import Certificate


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"


@login_required
def logout_user(request):
    logout(request)
    return redirect("login_url")


class MyCertificateView(LoginRequiredMixin, ListView):
    queryset = Certificate.objects.all()
    template_name = 'cli/my_certificate.html'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class MySubjectCertificateView(LoginRequiredMixin, ListView):
    queryset = Certificate.objects.all()
    template_name = 'cli/subject_certificate.html'

    def get_queryset(self):
        cert_pk = self.request.user.certificates.values_list('pk', flat=True)
        return self.queryset.filter(pk__in=cert_pk)


class EncryptFileView(LoginRequiredMixin, View):
    pass


class DecryptFileView(LoginRequiredMixin, View):
    pass
