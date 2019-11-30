from rest_framework.renderers import JSONRenderer
from rest_framework import status


class ProfileRenderer(JSONRenderer):
    """
    custom renderer class
    """

    def render(self, data, accepted_media_type=None, render_context=None):
        status_code = render_context["response"].status_code
        profile_id = render_context["kwargs"]["username"]
        operation = getattr(render_context["view"], "operation", None)

        def cleanErrorData(data: dict) -> dict:
            """
            remove empty objects in the present in response data
            """
            for (field, errors) in data.items():
                if isinstance(errors, list):
                    errors = list(filter(lambda value: value != {}, errors))
                    data[field] = errors
            error = data.get("error", data)
            return (
                {"message": data.pop("message"), "errors": data}
                if len(data) > 2
                else {"message": data.pop("message"), "error": error}
            )

        data = (
            {
                "message": "User Profile for user '%s'" % profile_id
                if render_context["request"].method == "GET"
                else "%s successfull" % operation,
                "data": data,
            }
            if status.is_success(status_code)
            else cleanErrorData(data)
            if (status_code == 404 or status_code == 422)
            else {"message": data["detail"]}
        )
        return super(ProfileRenderer, self).render(
            data, accepted_media_type, render_context
        )
