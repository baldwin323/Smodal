
```python
import pytest
import requests
from flask import Flask
from src.config import APP_CONFIG
from unittest.mock import patch, MagicMock

from src.social_media_integration import connect_to_social_media

@pytest.fixture
def client():
    Flask(__name__).config['TESTING'] = True
    with Flask(__name__).test_client() as client:
        yield client

@patch('requests.post')
def test_connect_to_social_media_valid(mock_post, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'access_token': 'test_access_token'}

    mock_post.return_value = mock_response

    response = client.post('/connect-social-media', json={'platform': 'twitter'})

    assert response.status_code == 200
    assert response.json == {'access_token': 'test_access_token'}

@patch('requests.post')
def test_connect_to_social_media_invalid(mock_post, client):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {'error': 'Invalid social media platform'}

    mock_post.return_value = mock_response

    response = client.post('/connect-social-media', json={'platform': 'invalid_platform'})

    assert response.status_code == 400
    assert response.json == {'error': 'Invalid social media platform'}

@patch('requests.post')
def test_connect_to_social_media_failed(mock_post, client):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {'error': 'Failed to connect to social media platform'}

    mock_post.return_value = mock_response

    response = client.post('/connect-social-media', json={'platform': 'twitter'})

    assert response.status_code == 500
    assert response.json == {'error': 'Failed to connect to social media platform'}
```
