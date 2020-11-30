"""
Authentication Functions
"""
from datetime import timedelta
from functools import wraps

from flask import abort
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request, get_raw_jwt, decode_token
)

from Delta3Mini.models.models import User

class AuthenticationError(Exception):
    """Base Authentication Exception"""
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.__class__.__name__ + '(' + str(self.msg) + ')'


class InvalidCredentials(AuthenticationError):
    """Invalid username/password"""


class AccountInactive(AuthenticationError):
    """Account is disabled"""


class AccessDenied(AuthenticationError):
    """Access is denied"""


class UserNotFound(AuthenticationError):
    """User identity not found"""


def get_authenticated_user():
    """
    Get authentication token user identity and verify account is active
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).scalar()
    if user is not None:
        return user
    else:
        raise UserNotFound(identity)


def refresh_authentication():
    """
    Refresh authentication, issue new access token
    """
    user = get_authenticated_user()
    return create_access_token(identity=user.id, expires_delta=timedelta(days=0, minutes=5))


def auth_required(func):
    """
    View decorator - require valid access token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        try:
            get_authenticated_user()
            refresh_authentication()
            return func(*args, **kwargs)
        except (UserNotFound, AccountInactive) as error:
            abort(403)
    return wrapper


def auth_refresh_required(func):
    """
    View decorator - require valid refresh token
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_refresh_token_in_request()
        try:
            get_authenticated_user()
            return func(*args, **kwargs)
        except (UserNotFound, AccountInactive) as error:
            abort(403)
    return wrapper

#
# def admin_required(func):
#     """
#     View decorator - required valid access token and admin access
#     """
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         verify_jwt_in_request()
#         try:
#             user = get_authenticated_user()
#             if user['is_admin']:
#                 return func(*args, **kwargs)
#             else:
#                 abort(403)
#         except (UserNotFound, AccountInactive) as error:
#             abort(403)
#     return wrapper