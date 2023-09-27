# File: watch_page_modal.py
# Defines the functions related to the main page such as:
# - Route to home page
# - Route to chat functionality for Live Chat Bot
# - Route to "Take Over Chat" button functionality
# - Route for modal to add necessary CSS and JavaScript files
# - Integrations with Github to get and edit open pull requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
from github import Github
import os

gh = Github()

def get_open_pull_requests(repository):
    repo = gh.get_repo(repository)
    return repo.get_pulls(state='open')

def edit_pull_request(repository, number, title=None):
    repo = gh.get_repo(repository)
    pr = repo.get_pull(number)
    if title is not None:
        pr.edit(title=title)
    return pr

class HomeView(View):
    template_name = 'watch_page.html'

    def get(self, request):
        return render(request, self.template_name)

class ChatView(View):
    def get(self, request):
        chat_message = "Your chat logic goes here"
        return JsonResponse({'chat_message': chat_message})

class TakeOverView(View):
    def get(self, request):
        takeover_message = "Logic to take over chat goes here."
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
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)