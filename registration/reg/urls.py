from django.urls import path

from . import views
from . import rest_views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', views.logout_user, name='logout_url'),
    path('certificate/', views.CertificateListView.as_view(), name='certificate_list_url'),
    path('certificate/<int:pk>', views.CertificateDetailView.as_view(), name='certificate_detail_url'),
    path('sas/', views.SasListView.as_view(), name='sas_list_url'),
    path('sas/as/<int:pk>', views.AsDetailView.as_view(), name='as_detail_url'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list_url'),
    path('subjects/<int:pk>', views.SubjectDetailView.as_view(), name='subject_detail_url'),
    path('history-registration/', views.HistoryRegistrationListView.as_view(), name='history_registration_list_url'),
    path('history-get-key/', views.HistoryGetKeyListView.as_view(), name='history_get_key_list_url'),
    path('api/registration/', rest_views.RegistrationView.as_view()),
    path('api/get-key/', rest_views.GetKeyView.as_view()),
    path('api/check-key/', rest_views.CheckKeyView.as_view()),
    path('api/cancellation/', rest_views.CancelledView.as_view()),
]
