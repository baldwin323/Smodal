```python
import json
import logging
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .ai_model import call_model
from .lambda_functions import give_credit, monitor_affiliated_models, register_affiliate_manager

from .models_file import (AIConversationModel, UserProfileModel, BankingModel, 
                          FileUploadModel, UIPageDataModel)
from .offline_utils import (authorize_request, check_authentication,
                            handle_user_login, handle_user_logout,
                            load_user_dashboard, perform_offline_login,
                            process_api_request)

# The address of the services
SERVICES_ADDRESS = os.getenv("SERVICES_ADDRESS", "localhost")
# The port where services are being served
SERVICES_PORT = os.getenv("SERVICES_PORT", "8000")
# Initializing logger for this file
logger = logging.getLogger(__name__)  

# User view functions classified according to their page
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
    response = register_affiliate_manager(request, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

@login_required
def affiliate_monitor(request):
    response = monitor_affiliated_models(request, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

@login_required
def affiliate_credit(request):
    response = give_credit(request, SERVICES_ADDRESS, SERVICES_PORT)
    return JsonResponse(response)

def is_authenticated(request):
    userid = request.session.get("user_id", None)
    return JsonResponse(check_authentication(userid, SERVICES_ADDRESS, SERVICES_PORT))

@login_required
def load_dashboard(request):
    userid = request.session.get("user_id", None)
    return JsonResponse(load_user_dashboard(userid, SERVICES_ADDRESS, SERVICES_PORT))

@require_POST
def login_user(request):
    """Handle user login requests"""
    if request.method == "POST":
        return JsonResponse(handle_user_login(request.POST, SERVICES_ADDRESS, SERVICES_PORT))
    
    # Return error if request is not POST
    return JsonResponse({"status": "error", "message": "You must submit a POST request."}, status=400)

def offline_login(request):
    """Handles offline user login"""
    user = perform_offline_login(request)
    if not user:
        return JsonResponse({'status': 'error', 'message': 'Could not authenticate user'}, status=401)

    # Log in user
    login(request, user)
    return JsonResponse({'status': 'success', 'user': user.username})

@login_required
def logout_user(request):
    """Handles user logout"""
    return JsonResponse(handle_user_logout(request.session.get("user_id", None), SERVICES_ADDRESS, SERVICES_PORT))

@login_required
def serve(request, page):
    """Handles requests for different pages"""
    if page not in PAGES:
        raise Http404

    page_spec = PAGES[page]

    # Check if user is authorized to access the page
    if page_spec['login_required']:
        response = authorize_request(request.session.get("user_id", None), SERVICES_ADDRESS, SERVICES_PORT)
        if response.get("status") != "success":
            return JsonResponse(response)

    # Try serving the page and return error if any issues occur
    try:
        return page_spec['method'](request)
    except Exception as e:
        logger.error(f"There was an error serving the page: {page}", exc_info=e)
        return JsonResponse({"status": "error", "message": "There was an error serving your request."}, status=500)

@login_required
def api_serve(request, page_id):
    """Handles API requests and returns a response"""
    if request.method == 'GET':
        return JsonResponse(process_api_request(request.GET, page_id, SERVICES_ADDRESS, SERVICES_PORT))
    
    # Return error if request is not GET
    return JsonResponse({"status": "error", "message": "Invalid request method. Only GET is supported."}, status=405)

@login_required
def ai_predict(request):
    """Uses AI model for prediction"""
    try:  
        input_data = request.GET.get('input')
        response = call_model(input_data, SERVICES_ADDRESS, SERVICES_PORT)

        # Use imported Pydantic model instead of Django model for conversation state
        conversation_state = AIConversationModel(user_id=request.user.profile, previous_responses=[], current_context=response)

    # Return error if any issues occur during prediction
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Could not process your request'}, status=500)

    return JsonResponse({'response': response})
```
