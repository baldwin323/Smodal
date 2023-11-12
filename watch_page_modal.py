import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
from github import Github
from Smodal.logging import logger 

# Alias to access Github API 
github_api = Github()

# Logger instance 
LOGGER = logging.getLogger(__name__)

# This function fetches all the open pull requests for a specific repository
def fetch_open_pull_requests(repository):
    """
    Fetch all open pull requests for the specified repository
    """
    try:
        # Access the repository using Github API
        repo = github_api.get_repo(repository)

        # Get all open pull requests from the repository
        pull_requests = repo.get_pulls(state='open')
        LOGGER.info("%s open pull requests found in %s.", len(pull_requests), repository)

        return pull_requests

    except Exception as error:
        # Log the error in case of any issue while fetching pull requests
        LOGGER.error("Failed to fetch open pull requests from %s: %s", repository, error)
        return JsonResponse({'error': str(error)}, status=400)

# This function modifies the title of a pull request
def modify_pull_request(repository, number, title=None):
    """
    Modify the title of a pull request
    """
    try:
        # Access the repository using Github API
        repo = github_api.get_repo(repository)

        # Get the pull request using its number
        pull_request = repo.get_pull(number)
        if title:
            # Modify the title of the pull request
            pull_request.edit(title=title)
        LOGGER.info("Pull request #%s title changed to %s.", number, title)

        return pull_request

    except Exception as error:
        # Log the error in case of any issue while modifying the pull request
        LOGGER.error("Failed to change pull request #%s title from %s: %s", number, repository, error)
        
        return JsonResponse({'error': str(error)}, status=400)

# Django view class for handling homepage requests
class HomePageView(View):
    template_name = 'watch_page.html'

    def get(self, request):
        """
        Handle GET request to the home page
        """
        try:
            # Render the home page using the specified template name
            return render(request, self.template_name)
        except Exception as error:
            # Log the error in case of any issue while rendering the page
            LOGGER.error("Failed to render %s: %s", self.template_name, error)

            return HttpResponse(status=500)

# Django view class for handling chat initiation requests
class ChatInitiationView(View):
    """
    Chat functionality for users
    """
    def get(self, request):
        """
        Handle GET request to initiate the chat
        """
        try:
            chat_message = "Chat here"
            LOGGER.info("Chat initiated.")

            return JsonResponse({'chat_message': chat_message})
        except Exception as error:
            # Log the error in case of any issue while initiating the chat
            LOGGER.error("Failed to initiate chat: %s", error)

            return HttpResponse(status=500)

# Django view class for handling chat takeover requests
class ChatTakeOverView(View):
    """
    Chat takeover functionality for users
    """
    def get(self, request):
        """
        Handle GET request to take over the chat
        """
        try:
            takeover_message = "Chat takeover logic"
            LOGGER.info("Chat taken over.")

            return JsonResponse({'takeover_message': takeover_message})
        except Exception as error:
            # Log the error in case of any issue while taking over the chat
            LOGGER.error("Failed to take over chat: %s", error)

            return HttpResponse(status=500)

# Django view class for handling modal view requests
class ModalDisplayView(View):
    template_name = 'modal.html'

    def get(self, request):
        """
        Handle GET request to render modal view
        """
        try:
            # Render the modal view using the specified template name
            return render(request, self.template_name)
        except Exception as error:
            # Log the error in case of any issue while rendering the modal view
            LOGGER.error("Failed to render %s: %s", self.template_name, error)

            return HttpResponse(status=500)

# Django URL routes for each view
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('chat/', ChatInitiationView.as_view(), name='chat'),
    path('takeover/', ChatTakeOverView.as_view(), name='takeover'),
    path('modal/', ModalDisplayView.as_view(), name='modal'),
]