from django.urls import path

from . import views
from . import rest_views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', views.logout_user, name='logout_url'),

    path('api/registration', rest_views.RegistrationView.as_view()),
    path('api/cancellation', rest_views.CancelledView.as_view())
]