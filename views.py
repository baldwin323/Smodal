import logging
from typing import Optional
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from .models import OIDCConfiguration, Credentials, APICredentials
from .logging import log_pactflow_response
import requests
import json

logger = logging.getLogger(__name__)

def social_media_login(request: HttpRequest, platform: str) -> Optional[HttpResponse]:
    """
    Manage login credentials for a specified social media platform.
    
    Checks the database for stored credentials or API keys corresponding
    to the requested platform and passes them for login.

    Args:
        request: HttpRequest object
        platform(str): Name of the social media platform.

    Returns:
        HttpResponse object if successful.
        None if an error occurred.
    """
    try:
        api_keys = APICredentials.objects.filter(platform=platform)
        if not api_keys.exists():
            login_details = Credentials.objects.filter(platform=platform)
            if not login_details.exists():
                raise Http404(f"No login credentials were found for {platform}.")
        return HttpResponse(f"Successfully fetched credentials for {platform}.")
    except Exception as e:
        logger.error(f"Error fetching credentials for {platform}: {str(e)}", exc_info=True)
        return HttpResponse(f"Could not fetch credentials for {platform} due to {str(e)}.", status=500)


def oidc_auth(request: HttpRequest) -> Optional[HttpResponse]:
    """
    Handle an OIDC authentication request from the client.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object if successful.
        None if an error occurred.
    """
    try:
        if not (config := OIDCConfiguration.objects.first()):
            raise Http404("No OIDC Configuration was found in the database.")
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()

        auth_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc"
   
        return redirect(
            f"{auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
    except Exception as e:
        logger.error(f"Error during OIDC Auth: {str(e)}", exc_info=True)
        return HttpResponse(f"An error occurred during OIDC authentication: {str(e)}.", status=500)


def oidc_callback(request: HttpRequest) -> Optional[HttpResponse]:
    """
    Handle the authorization server's callback.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object if successful.
        None if an error occurred.
    """
    try:
        if not (config := OIDCConfiguration.objects.first()):
            raise Http404("No OIDC Configuration was found in the database.")

        token_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc/token"
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()
        client_secret = config.client_secret

        code = request.GET.get('code')

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        body = {'grant_type': 'authorization_code', 
                'code': code, 
                'client_id': client_id, 
                'client_secret': client_secret, 
                'redirect_uri': redirect_uri }

        r = requests.post(token_url, headers=headers, data=body)

        if r.status_code != 200:
            raise Exception(f"Error retrieved during fetching tokens: {r.reason}, Response: {r.text}")

        access_token = r.json().get('access_token')
        access_token = "eyJhb...VFd1RiimyIT3zmFSEeP...tutmkZYVwR1mTgjGvJFC...UXqepbJx5ef"

        pactflow_headers = {'Authorization': f'Bearer {access_token}'}
        r_pactflow = requests.get('https://modaltokai-smodal.pactflow.io', headers=pactflow_headers)

        if r_pactflow.status_code != 200:
            raise Exception(f"Error retrieved during fetching data from Pactflow: {r_pactflow.reason}, Response: {r_pactflow.text}")

        response_headers = json.dumps(dict(r_pactflow.headers))
        response_body = json.dumps(r_pactflow.json())

        config.pactflow_response_headers = response_headers
        config.pactflow_response_body = response_body
        config.save()

        log_pactflow_response(response_headers, response_body)

        return redirect('/home/')
    except Exception as e:
        logger.error(f"Error during OIDC Callback: {str(e)}", exc_info=True)
        return HttpResponse(f"An error occurred during OIDC callback: {str(e)}.", status=500)