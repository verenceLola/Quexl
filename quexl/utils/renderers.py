from rest_framework import status
from rest_framework.renderers import JSONRenderer

message_map = lambda view: lambda status_code: {  # noqa
    "POST": "%s created successfully" % view.name.capitalize(),
    "PATCH": "%s updated succesfully" % view.name.capitalize(),
    "DELETE": "%s deleted successfully" % view.name.capitalize(),
}.get(status_code)


class DefaultRenderer(JSONRenderer):
    """
    custom renderer class for application views
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        format response data for application views
        """
        status_code = renderer_context["response"].status_code
        if renderer_context["request"].method == "GET":
            if renderer_context["kwargs"] == {}:
                message = (
                    "All %s"  # TODO fix bug for single and all orders views
                    % renderer_context["view"].pluralized_name.capitalize()
                )
            else:
                message = (
                    "%s info" % renderer_context["view"].name.capitalize()
                )
        else:
            message = message_map(renderer_context["view"])(
                renderer_context["request"].method
            )
        data = (
            ({"status": "success", "message": message, "data": data})
            if status.is_success(status_code)
            else {
                "status": "error",
                "message": "Correct the errors below",
                "data": data,
            }
        )
        return super(DefaultRenderer, self).render(
            data, accepted_media_type, renderer_context
        )
