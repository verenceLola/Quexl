"""
renderer for orders views
"""
from rest_framework import status
from rest_framework.renderers import JSONRenderer

message_map = lambda view: lambda status_code: {  # noqa
    "POST": "%s created successfully" % view.name.capitalize(),
    "PATCH": "%s updated succesfully" % view.name.capitalize(),
    "DELETE": "%s deleted successfully" % view.name.capitalize(),
}.get(status_code)


class OrdersRenderer(JSONRenderer):
    """
    custom renderer class for orders views
    """

    def render(self, data, accepted_media_type=None, render_context=None):
        """
        format response data for orders views
        """
        status_code = render_context["response"].status_code
        if render_context["request"].method == "GET":
            if render_context["kwargs"] == {}:
                message = (
                    "All %s"  # TODO fix bug for single and all orders views
                    % render_context["view"].pluralized_name.capitalize()
                )
            else:
                message = "%s info" % render_context["view"].name.capitalize()
        else:
            message = message_map(render_context["view"])(
                render_context["request"].method
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
        return super(OrdersRenderer, self).render(
            data, accepted_media_type, render_context
        )
