import logging
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.debug import ExceptionReporter
from django.contrib.auth.models import User
from .models import OIDCConfiguration, Credentials, APICredentials, AffiliateManager, UserProfile, FileUpload, UserActivity, Banking
import json

logger = logging.getLogger(__name__)

# Page mapping
PAGES = {
    'dashboard': {
        'method': lambda req: load_dashboard(req),
        'login_required': True
    },
    'login': {
        'method': lambda req: login_user(req),
        'login_required': False
    },
    'logout': {
        'method': lambda req: logout_user(req),
        'login_required': True
    },
}

def is_authenticated(request):
    return request.user.is_authenticated

@login_required
def load_dashboard(request):
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    return render(request, 'dashboard.html', {'user_profile': user_profile})

def login_user(req):
    if req.method == 'POST':
        email = req.POST.get('email', None)
        password = req.POST.get('password', None)
        # Authenticate user
        user = authenticate(req, username=email, password=password)
        if user is None:
            return render(req, 'login.html', {
                'error_message': 'Invalid credentials'
            })
        else:
            login(req, user)
            return render(req, 'dashboard.html')
    else:
        return render(req, 'login.html')

@login_required
def logout_user(req):
    logout(req)
    return render(req, 'login.html')

@login_required
def form_submit(request):
    pass  # Implement form functionality

@login_required
def file_upload(request):
    pass  # Implement file upload functionality

@login_required
def user_activity(request):
    user_activity = UserActivity.objects.filter(user_id=request.user.id)
    return render(request, 'activity.html', {'user_activity': user_activity})

@login_required
def banking(request):
    user_banking = Banking.objects.filter(user_id=request.user.id)
    return render(request, 'banking.html', {'user_banking': user_banking})

@login_required
def serve(request, page):
    if page in PAGES:
        return render(request, 'index.html')
    else:
        raise Http404

