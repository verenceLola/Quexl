import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict


class UserJSONRenderer(JSONRenderer):
    """
    Renderer which serializes data to JSON.
    """

    charset = "utf-8"

    def render(
        self,
        data: Union[
            Dict[str, ErrorDetail],
            ReturnDict,
            Dict[str, Union[str, List[ErrorDetail]]],
            Dict[str, Union[str, Dict[str, str]]],
            Dict[str, str],
        ],
        media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> Union[str, bytes]:
        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        status_code = renderer_context["response"].status_code

        return (
            json.dumps(data)
            if status.is_success(status_code)
            else super(UserJSONRenderer, self).render(
                {
                    "message": data.pop("message", "Fix the error(s) below"),
                    "errors": data,
                }
            )
        )
