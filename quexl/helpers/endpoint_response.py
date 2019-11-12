from rest_framework.response import Response


def get_success_responses(message, data, **kwargs):
    return Response(
        {"message": message, "data": data}, kwargs.get("status_code")
    )


def get_error_response(message, error, **kwargs):
    return Response(
        {"message": message, "error": error}, kwargs.get("status_code")
    )
