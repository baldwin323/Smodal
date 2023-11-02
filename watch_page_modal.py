import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
from github import Github
from Smodal.logging import logger 

LOG = logging.getLogger(__name__)

gh = Github()

# Fetches all open pull requests for a specific repository
def fetch_open_pull_requests(repository):
    """
    Fetch all open pull requests for the specified repository
    """
    try:
        repo = gh.get_repo(repository)
        pull_requests = repo.get_pulls(state='open')
        LOG.info("%s open pull requests found in %s.", len(pull_requests), repository)

        return pull_requests

    except Exception as error:
        # Error handling in case of any issue while fetching pull requests
        LOG.error("Failed to fetch open pull requests from %s: %s", repository, error)
        return JsonResponse({'error': str(error)}, status=400)

# Modifies the title of a pull request
def modify_pull_request(repository, number, title=None):
    """
    Modify the title of a pull request
    """
    try:
        repo = gh.get_repo(repository)
        pull_request = repo.get_pull(number)
        if title:
            pull_request.edit(title=title)
        LOG.info("Pull request #%s title changed to %s.", number, title)

        return pull_request

    except Exception as error:
        # Error handling in case of any issue while modifying the pull request
        LOG.error("Failed to change pull request #%s title from %s: %s", number, repository, error)
        
        return JsonResponse({'error': str(error)}, status=400)

# Django view class for handling home page requests
class HomeView(View):
    template_name = 'watch_page.html'

    def get(self, request):
        """
        Handle GET request to the home page
        """
        try:
            return render(request, self.template_name)
        except Exception as error:
            # Error handling in case of any issue while rendering the page
            LOG.error("Failed to render %s: %s", self.template_name, error)

            return HttpResponse(status=500)

# Django view class for handling chat requests
class ChatView(View):
    """
    Chat functionality for users
    """
    def get(self, request):
        """
        Handle GET request to initiate chat
        """
        try:
            chat_message = "Chat here"
            LOG.info("Chat initiated.")

            return JsonResponse({'chat_message': chat_message})
        except Exception as error:
            # Error handling in case of any issue while initiating chat
            LOG.error("Failed to initiate chat: %s", error)

            return HttpResponse(status=500)

# Django view class for handling chat takeover requests
class TakeOverView(View):
    """
    Chat takeover functionality for users
    """
    def get(self, request):
        """
        Handle GET request to take over chat
        """
        try:
            takeover_message = "Chat takeover logic"
            LOG.info("Chat taken over.")

            return JsonResponse({'takeover_message': takeover_message})
        except Exception as error:
            # Error handling in case of any issue while taking over chat
            LOG.error("Failed to take over chat: %s", error)

            return HttpResponse(status=500)

# Django view class for handling modal view requests
class ModalView(View):
    template_name = 'modal.html'

    def get(self, request):
        """
        Handle GET request to render modal view
        """
        try:
            return render(request, self.template_name)
        except Exception as error:
            # Error handling in case of any issue while rendering the modal view
            LOG.error("Failed to render %s: %s", self.template_name, error)

            return HttpResponse(status=500)

# Defining django url routes for each view
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('takeover/', TakeOverView.as_view(), name='takeover'),
    path('modal/', ModalView.as_view(), name='modal'),
]