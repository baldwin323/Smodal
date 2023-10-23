import logging
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from .models import OIDCConfiguration, Credentials, APICredentials, AffiliateManager, ManagedModels
import json
from django.contrib.auth.decorators import login_required
from django.views.debug import ExceptionReporter, get_exception_reporter_filter

logger = logging.getLogger(__name__)

# Page mapping
PAGES = {
    'index': {
        'method': lambda req: load_template('index.html'),
        'login_required': False
    },
    'login': {
        'method': lambda req: login(req),
        'login_required': False
    },
    'logout': {
        'method': lambda req: logout(req),
        'login_required': True
    },
    'affiliate_manager': {
        'method': lambda req: load_template('affiliate_manager.html'),
        'login_required': True
    },
    'new_feature': {
        'method': lambda req: load_template('new_feature.html'),
        'login_required': True,
        'admin_required': True
    },
    'another_new_feature': {
        'method': lambda req: load_template('another_new_feature.html'),
        'login_required': True,
        'admin_required': True
    }
}

def is_authenticated(request):
    return 'username' in request.session

def load_template(template:str):
    return render(request, template)

def require_login(func):
    def func_wrapper(request):
        if is_authenticated(request):
            return func(request)
        else:
            return load_template('login.html')
    return func_wrapper

def index(request):
    return PAGES['index']['method'](request)

@require_login
def logout(request):
    del request.session['username']
    return PAGES['logout']['method'](request)

@login_required
def form_submit(request):
    # Check for circular imports related issues 
    # process form
    return load_template('result.html')

def login(request):
    if is_authenticated(request):
        return PAGES['index']['method'](request)
    if request.method == 'POST':
        # Update login form processing methodology
        return load_template('login.html')

@login_required
def social_media_login(request: HttpRequest, platform: str) -> Optional[HttpResponse]:
    try:
        api_keys = APICredentials.objects.filter(platform=platform)
        login_details = None
        if not api_keys.exists():
            login_details = Credentials.objects.filter(platform=platform)
            if not login_details.exists():
                return JsonResponse({"error": f"No login credentials were found for {platform}."}, status=404)
        return JsonResponse({"success": f"Successfully fetched credentials for {platform}."}, status=200)
    except Exception as e:
        logger.error(f"Error fetching credentials for {platform}: {str(e)}", exc_info=True)
        return JsonResponse({"error": f"Could not fetch credentials for {platform} due to {str(e)}."}, status=500)

@login_required
def oidc_auth(request: HttpRequest) -> Optional[HttpResponse]:
    # OIDC logic

@login_required
def oidc_callback(request: HttpRequest) -> Optional[HttpResponse]:
    # OIDC callback logic

def render_page(request, page):
    if page in PAGES:
        page_cfg = PAGES[page]
        if page_cfg.get('login_required', False) and not is_authenticated(request):
            return redirect('login')
        return page_cfg['method'](request)
    else:
        return Http404

@login_required
def serve(request, page):
    return render_page(request, page)

@login_required
def new_feature(request):
    if 'admin' not in request.session['user'].groups: 
        return load_template('not_authorised.html')

    return PAGES['new_feature']['method'](request)

@login_required
def another_new_feature(request):
    if 'admin' not in request.session['user'].groups: 
        return load_template('not_authorised.html')
    
    return PAGES['another_new_feature']['method'](request)