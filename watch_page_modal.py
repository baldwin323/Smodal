import sys
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
from github import Github
from Smodal.logging import logger 

gh = Github()

def get_open_pull_requests(repository):
    """
    This function fetches all the open pull requests for a given repository
    :param repository: GitHub repository
    :return: returns the list of open pull requests
    """
    try:
        repo = gh.get_repo(repository)
        prs = repo.get_pulls(state='open')
        logger.info(f"{len(prs)} pull requests found in the repo: {repository}.")
        return prs
    except Exception as e:
        message = f"Failed to get open pull requests from {repository}: {str(e)}"
        logger.error(message)
        return JsonResponse({'error': message}, status=400)

def edit_pull_request(repository, number, title=None):
    """
    This function allows to edit the title of a given pull request number from the repository
    :param repository: GitHub repository
    :param number: Number of the pull request
    :param title: new title for the pull request
    :return: edited pull request object
    """
    try:
        repo = gh.get_repo(repository)
        pr = repo.get_pull(number)
        if title is not None:
            pr.edit(title=title)
        logger.info(
            f"The pull request number {number} has been edited with title: {title}"
        )
        return pr
    except Exception as e:
        message = f"Failed to edit pull request {number} from {repository}: {str(e)}"
        logger.error(message)
        return JsonResponse({'error': message}, status=400)

class HomeView(View):
    template_name = 'watch_page.html'

    def get(self, request):
        """
        GET method for the HomeView
        :param request: HTTP request
        :return: Rendered template or 500 HTTP response in case of error
        """
        try:
            return render(request, self.template_name)
        except Exception as e:
            message = f"Failed to render {self.template_name}: {str(e)}"
            logger.error(message)
            return HttpResponse(status=500)

class ChatView(View):
    def get(self, request):
        """
        GET method for the ChatView
        :param request: HTTP request
        :return: JsonResponse with chat message or 500 HTTP response in case of error
        """
        try:
            chat_message = "Your chat logic goes here"
            logger.info("Chat initiated.")
            return JsonResponse({'chat_message': chat_message})
        except Exception as e:
            message = f"Failed to initiate chat: {str(e)}"
            logger.error(message)
            return HttpResponse(status=500)

class TakeOverView(View):
    def get(self, request):
        """
        GET method for the TakeOverView
        :param request: HTTP request
        :return: JsonResponse with takeover message or 500 HTTP response in case of error
        """
        try:
            takeover_message = "Logic to take over chat goes here."
            logger.info("Chat taken over.")
            return JsonResponse({'takeover_message': takeover_message})
        except Exception as e:
            message = f"Failed to take over chat: {str(e)}"
            logger.error(message)
            return HttpResponse(status=500)

class ModalView(View):
    template_name = 'modal.html'

    def get(self, request):
        """
        GET method for the ModalView
        :param request: HTTP request
        :return: Rendered template or 500 HTTP response in case of error

        """
        try:
            return render(request, self.template_name)
        except Exception as e:
            message = f"Failed to render {self.template_name}: {str(e)}"
            logger.error(message)
            return HttpResponse(status=500)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('takeover/', TakeOverView.as_view(), name='takeover'),
    path('modal/', ModalView.as_view(), name='modal'),
]

if __name__ == '__main__':
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    from django.core.management import execute_from_command_line
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        message = f"Failed to run server: {str(e)}"
        logger.error(message)