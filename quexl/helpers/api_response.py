from typing import Dict
from typing import Union

from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.utils.serializer_helpers import ReturnList


class APIResponse:
    @staticmethod
    def get_success_responses(
        message: str,
        data: Union[Dict[str, bool], ReturnDict, ReturnList, Dict[str, str]],
        **kwargs,
    ) -> Response:
        return Response(
            {"message": message, "data": data}, kwargs.get("status_code")
        )

    @staticmethod
    def get_error_response(message: str, error: str, **kwargs) -> Response:
        return Response(
            {"message": message, "error": error}, kwargs.get("status_code")
        )
