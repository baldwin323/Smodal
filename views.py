
import logging
import json
import os  
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .lambda_functions import register_affiliate_manager, monitor_affiliated_models, give_credit
from .models import OIDCConfiguration, Credentials, APICredentials, AffiliateManager, UserProfile, FileUpload, UserActivity, Banking, AIConversation
from .offline_utils import perform_offline_login, handle_user_logout, check_authentication, authorize_request, load_user_dashboard, handle_user_login, process_api_request
from .ai_model import call_model  

SERVICES_ADDRESS = os.getenv("SERVICES_ADDRESS", "localhost")
SERVICES_PORT = os.getenv("SERVICES_PORT", "8000")

logger = logging.getLogger(__name__)

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
    user_id = request.session.get("user_id", None)
    return JsonResponse(check_authentication(user_id, SERVICES_ADDRESS, SERVICES_PORT))

@login_required
def load_dashboard(request):
    user_id = request.session.get("user_id", None)
    return JsonResponse(load_user_dashboard(user_id, SERVICES_ADDRESS, SERVICES_PORT))

@require_POST
def login_user(req):
    if req.method == "POST":
        return JsonResponse(handle_user_login(req.POST, SERVICES_ADDRESS, SERVICES_PORT))
    else:
        return JsonResponse({"status": "error", "message": "You must submit a POST request."}, status=400)


def offline_login(req):
    user = perform_offline_login(req)
    if not user:
        return JsonResponse({'status': 'error', 'message': 'Could not authenticate user'}, status=401)
    login(req, user)
    return JsonResponse({'status': 'success', 'user': user.username})

@login_required
def logout_user(req):
    return JsonResponse(handle_user_logout(req.session.get("user_id", None), SERVICES_ADDRESS, SERVICES_PORT))

@login_required
def serve(request, page):
    if page not in PAGES:
        raise Http404

    page_spec = PAGES[page]
    if page_spec['login_required']:
        response = authorize_request(request.session.get("user_id", None), SERVICES_ADDRESS, SERVICES_PORT)
        if response.get("status") != "success":
            return JsonResponse(response)

    try:
        return page_spec['method'](request)
    except Exception as e:
        logger.error(f"There was an error serving the page: {page}", exc_info=e)
        return JsonResponse({"status": "error", "message": "There was an error serving your request."}, status=500)

@login_required
def api_serve(request, page_id):
    if request.method == 'GET':
        return JsonResponse(process_api_request(request.GET, page_id, SERVICES_ADDRESS, SERVICES_PORT))
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method. Only GET is supported."}, status=405)

@login_required
def ai_predict(request):
    try:  
        input_data = request.GET.get('input')
        response = call_model(input_data, SERVICES_ADDRESS, SERVICES_PORT)
        
        conversation_state = AIConversation.objects.get(user_id=request.user.profile)
        conversation_state.previous_responses.append(response)
        conversation_state.current_context = response  
        conversation_state.save()
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Could not process your request'}, status=500)

    return JsonResponse({'response': response})