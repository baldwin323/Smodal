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
    path('index/', views.index, name='index'),
    path('form_submit/', views.form_submit, name='form_submit'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Add new paths for new frontend features
    path('new_feature/', views.new_feature, name='new_feature'),
    path('another_new_feature/', views.another_new_feature, name='another_new_feature'),
]