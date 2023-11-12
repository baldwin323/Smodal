import logging
import json
# Added import for third-party integrations
from social_django.utils import BACKENDS, backends_data, load_backend, load_strategy
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.debug import ExceptionReporter
from django.contrib.auth.models import User
from .lambda_functions import register_affiliate_manager, monitor_affiliated_models, give_credit
from .models import OIDCConfiguration, Credentials, APICredentials, AffiliateManager, UserProfile, FileUpload, UserActivity, Banking, AIConversation
from .offline_utils import perform_offline_login
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
    'offline_login': {
        'method': lambda req: offline_login(req),
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

def offline_login(req):
    """
    Handle User Login -- offline mode
    """
    # In offline mode, we assume the user is who they say they are without checking credentials
    user = perform_offline_login(req)
    if not user:
        return JsonResponse({'status': 'error', 'message': 'Could not authenticate user'}, status=401)
    login(req, user)
    return JsonResponse({'status': 'success', 'user': user.username})

@login_required
def logout_user(req):
    """
    Handle User Logout
    """
    logout(req)
    return render(req, 'login.html')

@login_required
def serve(request, page):
    """
    Functionality to serve a page
    """
    # Exclude these pages from requiring login
    if page not in PAGES:
        raise Http404

    page_spec = PAGES[page]
    if page_spec['login_required']:
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to access this page."}, status=401)
        
    try:
        return page_spec['method'](request, page)
    except Exception as e:
        logger.error(f"There was an error serving the page: {page}", exc_info=e)
        return JsonResponse({"status": "error", "message": "There was an error serving your request."}, status=500)

@login_required
def api_serve(request, page_id):
    """
    Functionality to serve a page via API endpoint.
    """
    # Check the request method
    if request.method == 'GET':
        try:
            # Here we simply return a JsonResponse object as a stub for each possible page_id.
            # In practice, implement the required API functionality for each page_id.
            response_data = {
                'user-authentication': {"data": "Stub data for user-authentication."},
                'dashboard': {"data": "Stub data for dashboard."},
                # Add similar responses for each page_id.
                'default': {"data": "Stub data for unknown page_id."},
            }
            return JsonResponse(response_data.get(page_id, response_data['default']))
        except Exception as e:
            logger.error("Error serving API page: {}".format(page_id), exc_info=e)

@login_required
def ai_predict(request):
    """
    Exposes an API endpoint for the trained AI model.
    """
    try:  # Handle potential errors
        # Extract the input data from the request
        input_data = request.GET.get('input')
        # Make a call to the AI model with the input data
        response = call_model(input_data)
        
        # Update the AI's conversation state in the database
        conversation_state = AIConversation.objects.get(user_id=request.user.profile)
        conversation_state.previous_responses.append(response)
        # Here we just set the AI's last response as current context,
        # but you should update context as per your AI model's requirements
        conversation_state.current_context = response  
        conversation_state.save()
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Could not process your request'}, status=500)
      
    return JsonResponse({'response': response})