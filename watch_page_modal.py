from pydantic import BaseModel, ValidationError
from modal.tokai.models import UserProfile, FileUpload, Banking, AIConversation, UIPageData
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from typing import Any, Dict, Union
import logging
from modal.tokai import logger 

# Alias to access Github API 
github_api = Github()

# Logger instance
# Updated from older version to reflect repo name change to modal.tokai
LOGGER = logging.getLogger(__name__)

def fetch_open_pull_requests(repository):
    """
    Fetch all open pull requests for the specified repository
    """
    try:
        # Access the repository using Github API
        repo = github_api.get_repo(repository)

        # Efficiently convert to list and return open pull requests
        pull_requests = list(repo.get_pulls(state='open'))
        LOGGER.info("%s open pull requests found in %s.", len(pull_requests), repository)

        return pull_requests

    except Exception as error:
        LOGGER.error("Failed to fetch open pull requests from %s: %s", repository, error)
        return {'error': str(error)}, 400

def modify_pull_request(repository, number, title=None):
    """
    Modify the title of a pull request
    """
    try:
        repo = github_api.get_repo(repository)

        pull_request = repo.get_pull(number)
        if title and title != pull_request.title:
            pull_request.edit(title=title)
        LOGGER.info("Pull request #%s title changed to %s.", number, title)

        return pull_request

    except Exception as error:
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
