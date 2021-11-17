from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from .models import Certificate
from .forms import AddSubjectCertificateForm
from .rest_tasks import *


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


class CancelledView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        cancellation.delay(
            subject_name = user.username,
            secret_key = user.secret_key,
            code = 6
        )
        return redirect('subject_certificates_url')


# class RegistrationCertificateView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         form = AddSubjectCertificateForm()
#         return render(request, )


class MySubjectCertificateView(LoginRequiredMixin, ListView):
    queryset = Certificate.objects.all()
    template_name = 'cli/subject_certificate.html'

    def get_queryset(self):
        cert_pk = self.request.user.certificates.values_list('pk', flat=True)
        return self.queryset.filter(pk__in=cert_pk)


class CheckKeyView(LoginRequiredMixin, View):

    def get(self, request, pk):
        certificate = Certificate.objects.get(pk=pk)
        check_key.delay(
            serial_number=certificate.serial_number
        )
        return redirect('subject_certificates_url')



class EncryptFileView(LoginRequiredMixin, View):
    pass


class DecryptFileView(LoginRequiredMixin, View):
    pass
