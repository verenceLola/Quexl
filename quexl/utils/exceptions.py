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
    "profiles": lambda response, **kwargs: get_error_response(
        "User profile %s does not exist" % kwargs["profile_id"],
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
            response, **context["kwargs"]
        )
    operation = context["view"].operation
    if isinstance(
        exc, ValidationError
    ):  # customize ValidationError exceptions
        return Response(
            {
                "message": "%s failed. Fix the error(s) below" % operation,
                **response.data,
            },
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return response
