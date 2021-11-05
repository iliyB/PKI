from django.urls import path

from. import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', views.logout_user, name='logout_url'),
    path('', views.CertificateListView.as_view(), name='certificate_list_url'),
    path('<int:pk>', views.CertificateDetailView.as_view(), name='certificate_detail_url')
]
