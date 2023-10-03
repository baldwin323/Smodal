# importing required libraries
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import OIDCConfiguration
import requests
import json

# Views for handling OIDC authentication flow

def oidc_auth(request):
    """ 
    View to handle initial OIDC authentication request.  
    """
    # Retrieve OIDC configuration from database.
    config = OIDCConfiguration.objects.first()
    if config:
        auth_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc"
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()
        
        # Constructing and redirecting to authentication URL.
        return redirect(auth_url+"?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code")
    else:
        return HttpResponse("OIDC Configuration not found in database.")

def oidc_callback(request):
    """
    View to handle auth server's callback
    """
    # Retrieve OIDC configuration from database.
    config = OIDCConfiguration.objects.first()
    if config:
        token_url = "https://api.bitbucket.org/2.0/workspaces/smodal/pipelines-config/identity/oidc/token"
        client_id = config.client_id
        redirect_uri = config.redirect_uris.split(',')[0].strip()
        client_secret = config.client_secret

        # Getting the authorization code from request parameters
        code = request.GET.get('code')

        # Constructing headers and body for token request.
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        body = {'grant_type': 'authorization_code', 'code': code, 'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri }

        # Making POST request to get tokens.
        r = requests.post(token_url, headers=headers, data=body)

        if r.status_code == 200:
            # If request is successful, redirect to home page after storing tokens.
            access_token = r.json().get('access_token')
            # Save pactflow response details
            r_pactflow = requests.get('https://modaltokai-smodal.pactflow.io')
            response_headers = json.dumps(dict(r_pactflow.headers))
            response_body = json.dumps(r_pactflow.json())
            config.pactflow_response_headers = response_headers
            config.pactflow_response_body = response_body
            config.save()
            # You may store the tokens in database for future use.
            # After storing the tokens, redirect as per your application's flow.
            return redirect('/home/')
        else:
            return HttpResponse("Error while fetching tokens. Please try again.")
    else:
        return HttpResponse("OIDC Configuration not found in database.")