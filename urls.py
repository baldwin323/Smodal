from django.urls import path
from . import views

# url patterns for the application
urlpatterns = [
    # path for oidc authentication
    path('oidc_auth/', views.oidc_auth, name='oidc_auth'),
    
    # path for oidc callback
    path('oidc_callback/', views.oidc_callback, name='oidc_callback'),
    
    # path for social media login for facebook
    path('social_login/facebook/', views.social_media_login, name='fb_login', kwargs={'platform': 'facebook'}),
    
    # path for social media login for twitter
    path('social_login/twitter/', views.social_media_login, name='twitter_login', kwargs={'platform': 'twitter'}),
    
    # path for social media login for instagram
    path('social_login/instagram/', views.social_media_login, name='instagram_login', kwargs={'platform': 'instagram'}),
    
    # path for social media login for linkedin
    path('social_login/linkedin/', views.social_media_login, name='linkedin_login', kwargs={'platform': 'linkedin'}),
    
    # path for social media login for google
    path('social_login/google/', views.social_media_login, name='google_login', kwargs={'platform': 'google'}),
]