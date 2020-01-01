from rest_framework import status
from rest_framework.renderers import JSONRenderer

from quexl.utils.errors import Errors


class ProfileRenderer(JSONRenderer):
    """
    custom renderer class
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        profile_id = renderer_context["kwargs"]["username"]
        operation = getattr(renderer_context["view"], "operation", None)

        data = (
            {
                "message": "User Profile for user '%s'" % profile_id
                if renderer_context["request"].method == "GET"
                else "%s successfull" % operation,
                "data": data,
            }
            if status.is_success(status_code)
            else Errors.cleanErrorData(data)
            if (status_code == 404 or status_code == 422)
            else {"message": data["detail"]}
        )

        return super(ProfileRenderer, self).render(
            data, accepted_media_type, renderer_context
        )
