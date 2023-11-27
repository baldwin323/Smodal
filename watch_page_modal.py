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

# This function fetches all the open pull requests for a specific repository.
# It's been optimised to directly return the list of pull requests instead of an iterator
def fetch_open_pull_requests(repository):
    """
    Fetch all open pull requests for the specified repository
    """
    try:
        # Access the repository using Github API
        repo = github_api.get_repo(repository)

        # Get all open pull requests from the repository. Converting to list for efficiency
        pull_requests = list(repo.get_pulls(state='open'))
        LOGGER.info("%s open pull requests found in %s.", len(pull_requests), repository)

        return pull_requests

    except Exception as error:
        # Log the error in case of any issue while fetching pull requests
        LOGGER.error("Failed to fetch open pull requests from %s: %s", repository, error)
        return {'error': str(error)}, 400

# This function modifies the title of a pull request
# Now includes a check to avoid unnecessary API calls if the new title is the same as the old one
def modify_pull_request(repository, number, title=None):
    """
    Modify the title of a pull request
    """
    try:
        # Access the repository using Github API
        repo = github_api.get_repo(repository)

        # Get the pull request using its number
        pull_request = repo.get_pull(number)
        if title and title != pull_request.title:
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
    Now using a dictionary for cleaner and more efficient model selection
    """
    try:
        models = {
            'UserProfile': UserProfile,
            'FileUpload': FileUpload,
            'Banking': Banking,
            'AIConversation': AIConversation,
            'UIPageData': UIPageData
        }

        if isinstance(model, str):
            model_to_validate = models.get(model)
            if not model_to_validate:
                raise ValidationError([ErrorWrapper(ValueError('Invalid model.'), loc='model')], model=BaseModel)

        model_to_validate(**data)

    except ValidationError as ve:
        LOGGER.error(f"Failed validation for {model}: {ve}")
        return {'error': str(ve)}, 400

    except Exception as ex:
        LOGGER.error(f"Failed to process {model}: {ex}")
        return {'error': str(ex)}, 400

    return {'data' : 'Validation passed.'}, 200

# No specific changes required for python 3.12 compatibility