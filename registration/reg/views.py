from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Certificate, Sas, Subject, HistoryRegistration, HistoryGetKey, As


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"


@login_required
def logout_user(request):
    logout(request)
    return redirect("login_url")


class CertificateListView(LoginRequiredMixin, ListView):
    model = Certificate

    def get_queryset(self):
        queryset = super(CertificateListView, self).get_queryset()
        subject = self.request.GET.get('subject', None)
        number = self.request.GET.get('number', None)
        if subject:
            return queryset.filter(subject_name__icontains=subject)
        elif number:
            return queryset.filter(serial_number__icontains=number)
        else:
            return queryset.all()


class CertificateDetailView(LoginRequiredMixin, DetailView):
    model = Certificate


class SasListView(LoginRequiredMixin, ListView):
    model = Sas


class AsDetailView(LoginRequiredMixin, DetailView):
    model = As


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject

    def get_queryset(self):
        queryset = super(SubjectListView, self).get_queryset()
        subject = self.request.GET.get('subject', None)
        if subject:
            return queryset.filter(subject_name__icontains=subject)
        else:
            return queryset.all()



class SubjectDetailView(LoginRequiredMixin, DetailView):
    model = Subject


class HistoryRegistrationListView(LoginRequiredMixin, ListView):
    model= HistoryRegistration

    def get_queryset(self):
        queryset = super(HistoryRegistrationListView, self).get_queryset()
        subject = self.request.GET.get('subject', None)
        if subject:
            return queryset.filter(subject__subject_name__icontains=subject)
        else:
            return queryset.all()



class HistoryGetKeyListView(LoginRequiredMixin, ListView):
    model = HistoryGetKey

    def get_queryset(self):
        queryset = super(HistoryGetKeyListView, self).get_queryset()
        subject = self.request.GET.get('subject', None)
        if subject:
            return queryset.filter(Q(subject__subject_name__icontains=subject) | Q(object__subject_name__icontains=subject))
        else:
            return queryset.all()
