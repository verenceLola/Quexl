"""
custom exception handler for views
"""
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import exception_handler

from quexl.helpers.api_response import APIResponse
from rest_framework import exceptions

view_map = {
    "profiles": lambda operation, response, **kwargs: APIResponse.get_error_response(
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


class NotGroupMember(exceptions.PermissionDenied):
    """
    user not authorized to access group
    """

    default_detail = "You're not a member of this group"
