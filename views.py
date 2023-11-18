import logging
import json
import os  # Added for environmental variables
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST  # Added this to enforce POST request method where required
from django.views.debug import ExceptionReporter
from django.contrib.auth.models import User
from .lambda_functions import register_affiliate_manager, monitor_affiliated_models, give_credit
from .models import OIDCConfiguration, Credentials, APICredentials, AffiliateManager, UserProfile, FileUpload, UserActivity, Banking, AIConversation
from .offline_utils import perform_offline_login
from .ai_model import call_model  # AI model function that generates predictions/responses

# Backend services address & port (from environment variables)
SERVICES_ADDRESS = os.getenv("SERVICES_ADDRESS", "localhost")
SERVICES_PORT = os.getenv("SERVICES_PORT", "8000")

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
    response = register_affiliate_manager(request, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

@login_required
def affiliate_monitor(request):
    """
    Function to monitor affiliated models
    """
    # Invoke the corresponding Lambda function
    response = monitor_affiliated_models(request, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

@login_required
def affiliate_credit(request):
    """
    Function to give credit when a new model signs up
    """
    # Invoke the corresponding Lambda function
    response = give_credit(request, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

def is_authenticated(request):
    """
    Checks if a user is authenticated
    """
    user_id = request.session.get("user_id", None)
    response = check_authentication(user_id, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

@login_required
def load_dashboard(request):
    """
    Load Dashboard for the authenticated user
    """
    # Load user's dashboard
    user_id = request.session.get("user_id", None)
    # Load data for the dashboard
    dashboard_data = load_user_dashboard(user_id, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(dashboard_data)

@require_POST  # Ensure POST method is used
def login_user(req):
    """
    Handle User Login
    """
    if req.method == "POST":
        response = handle_user_login(req.POST, SERVICES_ADDRESS, SERVICES_PORT)
        return JsonResponse(response)
    else:
        # Unnecessary now due to require_POST decorator
        return JsonResponse({"status": "error", "message": "You must submit a POST request."}, status=400)

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
    response = handle_user_logout(req.session.get("user_id", None), SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

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
        response = authorize_request(request.session.get("user_id", None), SERVICES_ADDRESS, SERVICES_PORT)
        if response.get("status") != "success":
            return JsonResponse(response)

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
        response = process_api_request(request.GET, page_id, SERVICES_ADDRESS, SERVICES_PORT)
        return JsonResponse(response)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method. Only GET is supported."}, status=405)

@login_required
def ai_predict(request):
    """
    Exposes an API endpoint for the trained AI model.
    """
    try:  # Handle potential errors
        # Extract the input data from the request
        input_data = request.GET.get('input')
        # Make a call to the AI model with the input data
        response = call_model(input_data, SERVICES_ADDRESS, SERVICES_PORT)
        
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