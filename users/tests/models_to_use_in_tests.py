import uuid

import pytest
from django.contrib.auth.models import User

from users.utils import get_tokens_for_user

CREATE_USER = {
    'username': str(uuid.uuid4()),
    'email': 'create@gmail.com',
    'password': "test_password",
    'password2': "test_password"
}
UPDATE_USER = {
    'username': str(uuid.uuid4()),
    'email': 'update@gmail.com',
    'password': "update_password",
    'password2': "update_password"
}
USER_WRONG_PASSWORD = {
    'username': str(uuid.uuid4()),
    'email': 'test2@gmail.com',
    'password': "first123",
    'password2': "first1234"
}
USER_SHORT_PASSWORD = {
    'username': str(uuid.uuid4()),
    'email': 'test2@gmail.com',
    'password': "first",
    'password2': "first"
}
USER_NUMBER_PASSWORD = {
    'username': str(uuid.uuid4()),
    'email': 'test2@gmail.com',
    'password': "555551111",
    'password2': "555551111"
}
USER_BLANK_USERNAME = {
    'username': '',
    'email': 'hgvh@gmail.com',
    'password': "first123",
    'password2': "first123"
}


