from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Certificate


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
        filter = self.request.GET.get('active', None)
        number = self.request.GET.get('number', None)

        if number:
            return queryset.filter(serial_number__icontains=number)
        elif subject:
            if filter is None:
                return queryset.filter(subject_name__icontains=subject)
            elif filter.lower() == 'true':
                return queryset.filter(active=True, subject_name__icontains=subject)
            elif filter.lower() == 'false':
                return queryset.filter(active=False, subject_name__icontains=subject)
            else:
                return queryset.filter(subject_name=subject)
        else:
            if filter is None:
                return queryset
            elif filter.lower() == 'true':
                return queryset.filter(active=True)
            elif filter.lower() == 'false':
                return queryset.filter(active=False)
            else:
                return queryset


class CertificateDetailView(LoginRequiredMixin, DetailView):
    model = Certificate
