import logging
from typing import Optional
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from .models import OIDCConfiguration, Credentials, APICredentials
from .logging import log_pactflow_response
import requests
import json

# Initialize the logger
logger = logging.getLogger(__name__)

def social_media_login(request: HttpRequest, platform: str) -> Optional[HttpResponse]:
    """
    Manage login credentials for social media site.

    Check for stored credentials or API keys within the 
    database and pass to the requested platform for login.

    Args:
        request: The HttpRequest object
        platform: str representing the social media site name

    Returns:
        Optional HttpResponse object indicating success or failure of operation
    """
    try:
        api_keys = APICredentials.objects.filter(platform=platform)
        if not api_keys.exists():
            login_details = Credentials.objects.filter(platform=platform)
            if not login_details.exists():
                raise Http404("No login credentials found for the requested platform.")
    except Exception as e:
        logger.error(f"Error fetching credentials: {str(e)}", exc_info=True)
        return HttpResponse(f"Error fetching credentials: {str(e)}", status=500)

def oidc_auth(request: HttpRequest) -> Optional[HttpResponse]:
    """ 
    Handle an initial OIDC authentication request.

    Args:
        request: The HttpRequest object 

    Returns:
        Optional HttpResponse object indicating success or failure of operation
    """
    try:
        if not (config := OIDCConfiguration.objects.first()):
            raise Http404("OIDC Configuration not in database.")
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()

        auth_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc"
   
        return redirect(
            f"{auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
    except Exception as e:
        logger.error(f"Error during OIDC Auth: {str(e)}", exc_info=True)
        return HttpResponse(f"Error during OIDC Auth: {str(e)}", status=500)

def oidc_callback(request: HttpRequest) -> Optional[HttpResponse]:
    """
    Manage auth server callback.

    Args:
        request: HttpRequest object

    Returns:
        Optional HttpResponse object indicating success or failure of operation
    """
    try:
        if not (config := OIDCConfiguration.objects.first()):
            raise Http404("OIDC Configuration not found in database.")
        token_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc/token"
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()
        client_secret = config.client_secret

        code = request.GET.get('code')

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        body = {'grant_type': 'authorization_code', 'code': code, 'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri }

        r = requests.post(token_url, headers=headers, data=body)

        if not r.ok:
            raise Exception("Error retrieved during fetching tokens: {0}, Response: {1}".format(r.reason, r.text))

        if r.status_code == 200:
            access_token = r.json().get('access_token')

            # Updated JWT Token
            access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRyaWFsIn0.eyJpc3MiOiJuZ2lueCBpc3N1ZXIiLCJpYXQiOjE2OTcyOTEwNDQsImp0aSI6IjE0ODM3Iiwic3ViIjoiVDAwMDEzMTk3NiIsImV4cCI6MTY5OTg4MzA0NH0.geiDEOEaxkk9naHlZI4pbBPRCChEJDKKLQSQebQeSfsn-uKk2fhqEEqUW3gLAN2r0j_uc2wgIlMgFPpDzmOf-1Nn6Dp54qfcUC8A2H59X7pkFhsaWRWGYPOn5peu3y8FPSo2a7gw77xOC2oz8o7iOhQYv4yb68bv2AWLepaGN0AsY4fr8tJykHrqmK6zN_1-85g9p-K50PzrEnHanO6WgmgSl6RxvCmIBlb6Hpeeb5bvm1kbsWgobpJSUXqepbJx5ef_YROGm93hVylnR80vCI53J-Ba0c6vJWrAec3sXmJQaDBjGYOl5mxueQWNz0cXNFd1RiimyIT3zmFSEePi71eatutmkZYVwR1mTgjGvJFCamZUWmeJ_o-N41l5I64_z-0sxIG9pjk8xC9EHhdqinikINcQ1s-jbTldG9aouDE8c9NG2jXumjV76CA6Xc3BD4-ciDLFIZrvbGX4H3dZgK141A6TUjnaO5AxP1UsDF1lLU-tE3vRMIxoR6VZzEKH"

            pactflow_headers = {'Authorization': f'Bearer {access_token}'}
            r_pactflow = requests.get('https://modaltokai-smodal.pactflow.io', headers=pactflow_headers)

            if not r_pactflow.ok:
                raise Exception("Error fetching data from Pactflow: {0}, Response: {1}".format(r_pactflow.reason, r_pactflow.text))

            if r_pactflow.status_code == 200:
                response_headers = json.dumps(dict(r_pactflow.headers))
                response_body = json.dumps(r_pactflow.json())

                config.pactflow_response_headers = response_headers
                config.pactflow_response_body = response_body
                config.save()

                log_pactflow_response(response_headers, response_body)
            else:
                return HttpResponse("Error fetching data from Pactflow. Try again.", status=500)

            return redirect('/home/')
        else:
            raise Exception("Error while fetching tokens")
    except Exception as e:
        logger.error(f"Error during OIDC Callback: {str(e)}", exc_info=True)
        return HttpResponse(f"Error during OIDC Callback: {str(e)}", status=500)