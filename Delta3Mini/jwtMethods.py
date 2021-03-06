"""
Authentication Functions
"""
from datetime import timedelta
from functools import wraps

from flask import abort, request
from flask_jwt_extended import (
    create_access_token, verify_fresh_jwt_in_request, decode_token, verify_jwt_refresh_token_in_request
)

from Delta3Mini.models.models import User, BlacklistToken


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


class TokenBlackListedFound(AuthenticationError):
    """Token was blacklisted"""


def get_authenticated_user(token):
    """
    Get authentication token user identity and verify account is active
    """
    identity = decode_token(token,allow_expired=True)
    user = User.query.filter_by(id=identity['sub']).scalar()
    if user is not None:
        return user
    else:
        raise UserNotFound(identity)


def refresh_authentication(old_token):
    """
    Refresh authentication, issue new access token
    """
    user = get_authenticated_user(old_token)
    BlacklistToken.add_to_db(old_token)
    return create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(days=0, minutes=5))


def auth_required(func):
    """
    View decorator - require valid access token
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_fresh_jwt_in_request()
            is_blacklisted_token = BlacklistToken.check_blacklist(request.headers.get('Authorization').split(" ")[1])
            if is_blacklisted_token:
                abort(401)
            return func(*args, **kwargs)
        except (UserNotFound, AccountInactive) as error:
            abort(403)
    return wrapper


def auth_fresh_required(func):
    """
    View decorator - require valid refresh token
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_refresh_token_in_request()
        return func(*args, **kwargs)
    return wrapper

# may be used in future but not now
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
#             app.logger.error('authorization failed: %s', error)
#             abort(403)
#     return wrapper
