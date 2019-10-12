from rest_framework.response import Response


def get_success_responses(message, data, **kwargs):
    return Response(
        {"message": message, "data": data}, kwargs.get("status_code")
    )


def get_error_response(message, **kwargs):
    return Response(({"message": message}, kwargs.get("status_code")))
