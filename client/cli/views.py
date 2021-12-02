from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from Crypto.PublicKey import RSA

from .models import Certificate, File
from .forms import AddSubjectCertificateForm, FileForm
from .rest_tasks import *
from .utils import edit_current_time
from .tasks import delete_file


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


class RegistrationCertificateView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        private_key = RSA.import_key(
            open(user.private_key.path).read(),
        )
        public_key = private_key.public_key().export_key('PEM')
        registration.delay(
            subject_name = user.username,
            public_key = public_key.decode(),
            secret_key = user.secret_key
        )
        return redirect('subject_certificates_url')


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


class GetKeyView(LoginRequiredMixin, View):

    def get(self, request):
        subject = request.GET.get('subject', None)

        if subject is not "":

            get_key.delay(
                subject_name = request.user.username,
                object_name = subject
            )
            return redirect('subject_certificates_url')

        return redirect('subject_certificates_url')


class EncryptFileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
         return render(request, 'cli/encrypt.html', context={'form': FileForm()})

    def post(self, request, *args, **kwargs):
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            subject_name = form.cleaned_data.pop('subject_name')

            user = request.user
            subject_certificate = user.certificates.filter(subject_name=subject_name)

            if not subject_certificate.exists():
                form.add_error('subject_name', 'Нет сертификата данного пользователя')
                return render(request, 'cli/encrypt.html', context={'form': form})

            instance = form.save()

            private_key = RSA.import_key(
                open(user.private_key.path).read()
            )

            public_key = RSA.import_key(
                subject_certificate.last().public_key
            )

            instance.encrypt(private_key, public_key)
            delete_file.delay(instance.pk, eta=edit_current_time() + timezone.timedelta(minutes=30))

            return render(request, 'cli/encrypt.html', context={'file': instance})

        return render(request, 'cli/encrypt.html', context={'form': form})


class DecryptFileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'cli/decrypt.html', context={'form': FileForm()})

    def post(self, request, *args, **kwargs):
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            subject_name = form.cleaned_data.pop('subject_name')

            user = request.user

            subject_certificate = user.certificates.filter(subject_name=subject_name)

            if not subject_certificate.exists():
                form.add_error('subject_name', 'Нет сертификата данного пользователя')
                return render(request, 'cli/decrypt.html', context={'form': form})

            instance = form.save()

            private_key = RSA.import_key(
                open(user.private_key.path).read()
            )

            public_key = RSA.import_key(
                subject_certificate.last().public_key
            )

            if not instance.decrypt(private_key, public_key):
                form.add_error('subject_name', 'Электронная подпись не совпадает')
            delete_file.delay(instance.pk, eta=edit_current_time() + timezone.timedelta(minutes=30))

            return render(request, 'cli/decrypt.html', context={'form': form, 'file': instance})

        return render(request, 'cli/decrypt.html', context={'form': form})
