"""
renderer for services views
"""
from rest_framework.renderers import JSONRenderer
from rest_framework import status


message_map = {
    "category": lambda status_code: {
        "POST": "Category created successfully",
        "PATCH": "Catergory updated succesfully",
        "DELETE": "Category deleted successfully",
        "GET": "All Categories",
    }.get(status_code)
}


class ServicesRenderer(JSONRenderer):
    """
    custom renderer class for services views
    """

    def render(self, data, accepted_media_type=None, render_context=None):
        """
        format response data for services views
        """
        status_code = render_context["response"].status_code
        data = (
            (
                {
                    "status": "success",
                    "message": message_map.get(render_context["view"].name)(
                        render_context["request"].method
                    ),
                    "data": data,
                }
            )
            if status.is_success(status_code)
            else {
                "status": "error",
                "message": "Correct the errors below",
                "data": data,
            }
        )
        return super(ServicesRenderer, self).render(
            data, accepted_media_type, render_context
        )
