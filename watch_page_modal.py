import logging
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
from github import Github
from Smodal.logging import logger 

LOG = logging.getLogger(__name__)

gh = Github()

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
        LOG.error("Failed to fetch open pull requests from %s: %s", repository, error)

        return JsonResponse({'error': str(error)}, status=400)

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
        LOG.error("Failed to change pull request #%s title from %s: %s", number, repository, error)
        
        return JsonResponse({'error': str(error)}, status=400)

class HomeView(View):
    template_name = 'watch_page.html'

    def get(self, request):
        """
        Handle GET request
        """
        try:
            return render(request, self.template_name)
        except Exception as error:
            LOG.error("Failed to render %s: %s", self.template_name, error)

            return HttpResponse(status=500)

class ChatView(View):
    """
    View for chat functionality
    """
    def get(self, request):
        """
        Handle GET request
        """
        try:
            chat_message = "Chat here"

            LOG.info("Chat initiated.")

            return JsonResponse({'chat_message': chat_message})
        except Exception as error:
            LOG.error("Failed to initiate chat: %s", error)

            return HttpResponse(status=500)

class TakeOverView(View):
    """
    View for chat takeover functionality
    """
    def get(self, request):
        """
        Handle GET request
        """
        try:
            takeover_message = "Chat takeover logic"

            LOG.info("Chat taken over.")

            return JsonResponse({'takeover_message': takeover_message})
        except Exception as error:
            LOG.error("Failed to take over chat: %s", error)

            return HttpResponse(status=500)

class ModalView(View):
    template_name = 'modal.html'

    def get(self, request):
        """
        Handle GET request
        """
        try:
            return render(request, self.template_name)
        except Exception as error:
            LOG.error("Failed to render %s: %s", self.template_name, error)

            return HttpResponse(status=500)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('takeover/', TakeOverView.as_view(), name='takeover'),
    path('modal/', ModalView.as_view(), name='modal'),
]