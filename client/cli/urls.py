from django.urls import path

from . import views
from . import rest_views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', views.logout_user, name='logout_url'),
    path('my-certificate/', views.MyCertificateView.as_view(), name='my_certificate_url'),
    path('subject-certificates/', views.MySubjectCertificateView.as_view(), name='subject_certificates_url'),
    path('encrypt/', views.EncryptFileView.as_view(), name='encrypt_url'),
    path('decrypt/', views.DecryptFileView.as_view(), name='decrypt_url'),

    path('registration/', views.RegistrationCertificateView.as_view(), name='registration_url'),
    path('cancellation/', views.CancelledView.as_view(), name='cancellation_url'),
    path('check-key/<int:pk>/', views.CheckKeyView.as_view(), name='check_key_url'),
    path('get-key/', views.GetKeyView.as_view(), name='get_key_url'),

    path('api/registration/', rest_views.RegistrationView.as_view()),
    path('api/cancellation/', rest_views.CancelledView.as_view())
]