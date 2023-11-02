import logging
import json
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.debug import ExceptionReporter
from django.contrib.auth.models import User
from .lambda_functions import register_affiliate_manager, monitor_affiliated_models, give_credit
from .models import OIDCConfiguration, Credentials, APICredentials, AffiliateManager, UserProfile, FileUpload, UserActivity, Banking, AIConversation
from .ai_model import call_model  # AI model function that generates predictions/responses
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

@login_required
def affiliate_register(request):
    """
    Function to register affiliate manager
    """
    # Invoke the corresponding Lambda function
    response = register_affiliate_manager(**request.POST)
    return JsonResponse(response)

@login_required
def affiliate_monitor(request):
    """
    Function to monitor affiliated models
    """
    # Invoke the corresponding Lambda function
    response = monitor_affiliated_models(**request.POST)
    return JsonResponse(response)

@login_required
def affiliate_credit(request):
    """
    Function to give credit when a new model signs up
    """
    # Invoke the corresponding Lambda function
    response = give_credit(**request.POST)
    return JsonResponse(response)

def is_authenticated(request):
    """
    Checks if a user is authenticated
    """
    return request.user.is_authenticated

@login_required
def load_dashboard(request):
    """
    Load Dashboard for the authenticated user
    """
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    return render(request, 'dashboard.html', {'user_profile': user_profile})

def login_user(req):
    """
    Handle User Login
    """
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
    """
    Handle User Logout
    """
    logout(req)
    return render(req, 'login.html')

@login_required
def form_submit(request):
    """
    Functionality for form submission
    """
    pass

@login_required
def file_upload(request):
    """
    Functionality for file upload
    """
    pass

@login_required
def user_activity(request):
    """
    Displays the user activity
    """
    user_activity = UserActivity.objects.filter(user_id=request.user.id)
    return render(request, 'activity.html', {'user_activity': user_activity})

@login_required
def banking(request):
    """
    Displays user's banking related data
    """
    user_banking = Banking.objects.filter(user_id=request.user.id)
    return render(request, 'banking.html', {'user_banking': user_banking})

@login_required
def serve(request, page):
    """
    Functionality to serve a page
    """
    if page in PAGES:
        return render(request, 'index.html')
    else:
        raise Http404

@login_required
def ai_predict(request):
    """
    Exposes an API endpoint for the trained AI model.
    """
    # Extract the input data from the request
    input_data = request.GET.get('input')
    
    # Make a call to the AI model with the input data
    response = call_model(input_data)
    
    # Update the AI's conversation state in the database
    conversation_state = AIConversation.objects.get(user_id=request.user.profile)
    conversation_state.previous_responses.append(response)
    conversation_state.current_context = response  # Here we just set the AI's last response as current context,
                                                   # but you should update context as per your AI model's requirements
    conversation_state.save()

    # Send back the response
    return JsonResponse({'response': response})