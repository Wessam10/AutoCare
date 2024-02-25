from rest_framework.exceptions import ValidationError, PermissionDenied, APIException
from rest_framework.views import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from logging import getLogger

from rest_framework.exceptions import ValidationError, PermissionDenied, APIException
from rest_framework.views import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from logging import getLogger

logger = getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Handles various exceptions and returns appropriate responses.

    Args:
        exc: The exception object that occurred.
        context: A dictionary containing request-related information.

    Returns:
        A Django Response object with the appropriate status code and error message.
    """

    # Access request object from the context
    request = context.get('request')

    # Handle specific exceptions:
    if isinstance(exc, ValidationError):
        response = Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, PermissionDenied):
        response = Response({"detail": "Unauthorized"},
                            status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, ObjectDoesNotExist):
        response = Response({"detail": "Resource not found"},
                            status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, APIException):
        response = Response({"detail": str(exc)}, status=exc.status_code)
    elif isinstance(exc, Exception) and request.user == AnonymousUser:
        # Handle unauthenticated users with a specific error message
        response = Response({"detail": "Authentication required"},
                            status=status.HTTP_401_UNAUTHORIZED)
    else:
        # Handle other unexpected errors (500 Internal Server Error)
        logger.error(f"Unexpected error: {exc}")
        response = Response("An internal error occurred",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
