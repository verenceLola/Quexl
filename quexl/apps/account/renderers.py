import json

from rest_framework import status
from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    """
    Renderer which serializes data to JSON.
    """

    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
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
