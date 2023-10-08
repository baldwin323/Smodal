from typing import Callable
from django.urls import path
from . import views

# URL patterns for the application
urlpatterns = [
    # Path for OIDC authentication
    # This route initiates oidc authentication process, returning a redirect response to the OIDC provider's authorization endpoint
    path('oidc_auth/', views.oidc_auth, name='oidc_auth'),

    # Path for OIDC callback
    # This route is the callback endpoint for OIDC providers. It processes the response from OIDC provider after the user has authenticated
    path('oidc_callback/', views.oidc_callback, name='oidc_callback'),

    # Path for social media login with Facebook
    # This route initiates the social media login process for Facebook, returning a redirect to Facebook's login endpoint
    path('social_login/facebook/', views.social_media_login, name='fb_login', kwargs={'platform': 'facebook'}),

    # Path for social media login with Twitter
    # This route initiates the social media login process for Twitter, returning a redirect to Twitter's login endpoint
    path('social_login/twitter/', views.social_media_login, name='twitter_login', kwargs={'platform': 'twitter'}),

    # Path for social media login with Instagram
    # This route initiates the social media login process for Instagram, returning a redirect to Instagram's login endpoint
    path('social_login/instagram/', views.social_media_login, name='instagram_login', kwargs={'platform': 'instagram'}),

    # Path for social media login with LinkedIn
    # This route initiates the social media login process for LinkedIn, returning a redirect to LinkedIn's login endpoint
    path('social_login/linkedin/', views.social_media_login, name='linkedin_login', kwargs={'platform': 'linkedin'}),

    # Path for social media login with Google
    # This route initiates the social media login process for Google, returning a redirect to Google's login endpoint
    path('social_login/google/', views.social_media_login, name='google_login', kwargs={'platform': 'google'}),
]