import logging
from typing import Optional
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from . models import OIDCConfiguration, Credentials, APICredentials
from .logging import log_pactflow_response
import requests
import json

logger = logging.getLogger(__name__)

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


def oidc_auth(request: HttpRequest) -> Optional[HttpResponse]:
    try:
        if not (config := OIDCConfiguration.objects.first()):
            return JsonResponse({"error": "No OIDC Configuration found."}, status=404)
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()

        auth_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc"
        return redirect(
            f"{auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code",
            status=307
        )
    except Exception as e:
        logger.error(f"Error during OIDC Auth: {str(e)}", exc_info=True)
        return JsonResponse({"error": f"An error occurred during OIDC authentication: {str(e)}."}, status=500)


def oidc_callback(request: HttpRequest) -> Optional[HttpResponse]:
    try:
        if not (config := OIDCConfiguration.objects.first()):
            return JsonResponse({"error": "No OIDC Configuration found."}, status=404)

        code = request.GET.get('code')
        if not code:
            return JsonResponse({"error": "No authentication code received from the OIDC provider."}, status=500)

        token_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc/token"
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()
        client_secret = config.client_secret

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri
        }

        r = requests.post(token_url, headers=headers, data=body)

        if r.status_code != 200:
            logger.error(f"Error while retrieving tokens from the OIDC provider. Response status code: {r.status_code}. Response text: {r.text}.")
            return JsonResponse(
                {
                    "error": f"Error retrieved during fetching tokens: {r.reason}"
                },
                status=r.status_code
            )

        access_token = r.json().get('access_token')

        pactflow_headers = {'Authorization': f'Bearer {access_token}'}
        r_pactflow = requests.get('https://modaltokai-smodal.pactflow.io', headers=pactflow_headers)

        if r_pactflow.status_code != 200:
            logger.error(f"Error while retrieving data from Pactflow. Response status code: {r_pactflow.status_code}. Response text: {r_pactflow.text}.")
            return JsonResponse(
                {
                    "error": f"Error retrieved during fetching data from Pactflow: {r_pactflow.reason}"
                },
                status=r_pactflow.status_code
            )

        response_headers = json.dumps(dict(r_pactflow.headers))
        response_body = json.dumps(r_pactflow.json())

        config.pactflow_response_headers = response_headers
        config.pactflow_response_body = response_body
        config.save()

        log_pactflow_response(response_headers, response_body)

        return redirect('/home/')
    except Exception as e:
        logger.error(f"Error during OIDC Callback: {str(e)}", exc_info=True)
        return JsonResponse({"error": f"An error occurred during OIDC callback: {str(e)}."}, status=500)