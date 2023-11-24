import os
from datetime import date
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
import secrets

# Fetch environment variables & setting default values
os.environ.get('DB_HOST', 'localhost')
os.environ.get('DB_PORT', '5432')


class UserProfile(BaseModel):
    # UserProfile model to store the user's details like dob, image, preferences etc. using Pydantic BaseModel
    birth_date: Optional[date] = Field(None, validate_format('%m-%d-%Y'))
    image: Optional[str] = Field(None, validate_format('.+\.((png)|(jpg))$'))
    preferences: Optional[Dict] = Field(None)
    theme_preferences: str = Field("default")


class FileUpload(BaseModel):
    # Model to store uploaded files using Pydantic BaseModel and added validation
    file: Optional[str] = Field(None, description='uploaded file path')
    token: str = Field(default_factory=secrets.token_urlsafe)

    # Adding a custom validator to check for allowed extensions
    @validator('file')
    def check_file_extension(cls, v):
        allowed_extensions = ['pdf', 'doc', 'jpg', 'png']
        if not v.split(".")[-1] in allowed_extensions:
            raise ValueError('Invalid file extension. Please upload a pdf, doc, jpg or png file.')
        return v


class Banking(BaseModel):
    transactions: Dict = Field(default_factory=dict)


class AIConversation(BaseModel):
    user_id: int = Field(...)  # Representing Foreign Key relation 
    previous_responses: List = Field(default_factory=list)
    current_context: str = Field(...)

    # Adding a validator to assert that user_id is positive integer
    @validator('user_id')
    def check_positive(cls, v):
        if v <= 0:
            raise ValueError('user_id must be a positive integer')
        return v


class UIPageData(BaseModel):
    page_id: str = Field(...)
    page_data: Dict = Field(default_factory=dict)


# Export the models
UserProfileModel = UserProfile.schema_json()
FileUploadModel = FileUpload.schema_json()
BankingModel = Banking.schema_json()
AIConversationModel = AIConversation.schema_json()
UIPageDataModel = UIPageData.schema_json()