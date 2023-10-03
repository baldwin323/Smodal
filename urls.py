from django.urls import path
from . import views

urlpatterns = [
    path('oidc_auth/', views.oidc_auth, name='oidc_auth'),
    path('oidc_callback/', views.oidc_callback, name='oidc_callback'),
]