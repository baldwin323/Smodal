from django.urls import path
from . import views

urlpatterns = [
    path('oidc_auth/', views.oidc_auth, name='oidc_auth'),
    path('oidc_callback/', views.oidc_callback, name='oidc_callback'),
    path('social_login/facebook/', views.social_media_login, name='fb_login', kwargs={'platform': 'facebook'}),
    path('social_login/twitter/', views.social_media_login, name='twitter_login', kwargs={'platform': 'twitter'}),
    path('social_login/instagram/', views.social_media_login, name='instagram_login', kwargs={'platform': 'instagram'}),
    path('social_login/linkedin/', views.social_media_login, name='linkedin_login', kwargs={'platform': 'linkedin'}),
    path('social_login/google/', views.social_media_login, name='google_login', kwargs={'platform': 'google'}),
]