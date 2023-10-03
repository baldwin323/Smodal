
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
from github import Github
from Smodal.logging import logger  # Use centralized logger

gh = Github()

def get_open_pull_requests(repository):
    repo = gh.get_repo(repository)
    prs = repo.get_pulls(state='open')
    logger.info("{} pull requests found in the repo: {}.".format(len(prs), repository))
    return prs

def edit_pull_request(repository, number, title=None):
    repo = gh.get_repo(repository)
    pr = repo.get_pull(number)
    if title is not None:
        pr.edit(title=title)
        logger.info("The pull request number {} has been edited with title: {}".format(number, title))
    return pr

class HomeView(View):
    template_name = 'watch_page.html'

    def get(self, request):
        return render(request, self.template_name)

class ChatView(View):
    def get(self, request):
        chat_message = "Your chat logic goes here"
        logger.info("Chat initiated.")
        return JsonResponse({'chat_message': chat_message})

class TakeOverView(View):
    def get(self, request):
        takeover_message = "Logic to take over chat goes here."
        logger.info("Chat taken over.")
        return JsonResponse({'takeover_message': takeover_message})

class ModalView(View):
    template_name = 'modal.html'

    def get(self, request):
        return render(request, self.template_name)

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
    execute_from_command_line(sys.argv)