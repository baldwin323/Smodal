import os
from datetime import date
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
import secrets

# Fetch environment variables & setting default values
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')


class UserProfile(BaseModel):
    """UserProfile model to store the user's details."""
    birth_date: Optional[date] = Field(None, format='%m-%d-%Y')
    image: Optional[str] = Field(None, format='.+\.((png)|(jpg))$')
    preferences: Optional[Dict] = Field(None)
    theme_preferences: str = Field("default")


class FileUpload(BaseModel):
    """Model to store uploaded files."""
    file: Optional[str] = Field(None, description='uploaded file path')
    token: str = Field(default_factory=secrets.token_urlsafe)

    @validator('file')
    def check_file_extension(cls, v):
        """Check file extension."""
        allowed_extensions = ['pdf', 'doc', 'jpg', 'png']
        if not v.split(".")[-1] in allowed_extensions:
            raise ValueError('Invalid file extension. Please upload a pdf, doc, jpg or png file.')
        return v


class Banking(BaseModel):
    """Model to keep track of banking transactions."""
    transactions: Dict = Field(default_factory=dict)


class AIConversation(BaseModel):
    """Model for keeping track of AI conversation."""
    user_id: int = Field(...) 
    previous_responses: List = Field(default_factory=list)
    current_context: str = Field(...)

    @validator('user_id')
    def check_positive(cls, v):
        """Assert user_id is positive."""
        if v <= 0:
            raise ValueError('user_id must be a positive integer')
        return v


class UIPageData(BaseModel):
    """Model for UI page data."""
    page_id: str = Field(...)
    page_data: Dict = Field(default_factory=dict)


# Export the models
UserProfileModel = UserProfile.schema_json()
FileUploadModel = FileUpload.schema_json()
BankingModel = Banking.schema_json()
AIConversationModel = AIConversation.schema_json()
UIPageDataModel = UIPageData.schema_json()