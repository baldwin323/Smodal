from pydantic import BaseModel, ValidationError
from Smodal.models import UserProfile, FileUpload, Banking, AIConversation, UIPageData
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from typing import Any, Dict, Union
import logging
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
        return {'error': str(error)}, 400

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

        return {'error': str(error)}, 400

def determine_model(model: Union[str, BaseModel], data: Dict[str, Any]):
    """
    Given a model and data, determines the kind of model and validates its data
    """
    try:
        if isinstance(model, str):
            if (model == 'UserProfile'):
                model = UserProfile
            elif (model == 'FileUpload'):
                model = FileUpload
            elif (model == 'Banking'):
                model = Banking
            elif (model == 'AIConversation'):
                model = AIConversation
            elif (model == 'UIPageData'):
                model = UIPageData
            else:
                raise ValidationError([ErrorWrapper(ValueError('Invalid model.'), loc='model')], model=BaseModel)
            
        model(**data)

    except ValidationError as ve:
        LOGGER.error(f"Failed validation for {model}: {ve}")
        return {'error': str(ve)}, 400

    except Exception as ex:
        LOGGER.error(f"Failed to process {model}: {ex}")
        return {'error': str(ex)}, 400

    return {'data' : 'Validation passed.'}, 200

# No specific changes required for python 3.12 compatibility