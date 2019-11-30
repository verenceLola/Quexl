"""
custom exception handler for views
"""
from rest_framework.views import exception_handler
from quexl.helpers.endpoint_response import get_error_response
from django.http import Http404
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework import status

view_map = {
    "profiles": lambda operation, response, **kwargs: get_error_response(
        "%s failed. Fix the error(s) below" % operation,
        "Profile for username '%s' does not exist" % kwargs["username"],
        status_code=response.status_code,
    )
}


def custom_exception_handler(exc, context):
    """
    custom exception handler for views
    """
    response = exception_handler(exc, context)
    if isinstance(exc, Http404):  # Customize Http404 exceptions
        return view_map.get(context["view"].name)(
            context["view"].operation, response, **context["kwargs"]
        )
    if isinstance(
        exc, ValidationError
    ):  # customize ValidationError exceptions
        operation = context[
            "view"
        ].operation  # every view method should have an operation
        return Response(
            {
                "message": "%s failed. Fix the error(s) below" % operation,
                **response.data,
            },
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return response
