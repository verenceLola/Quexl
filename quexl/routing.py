import quexl.apps.messaging.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from quexl.apps.messaging.middlewares import JWTAuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator


application = ProtocolTypeRouter(
    {
        # WebSocket message handler
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddlewareStack(
                URLRouter(quexl.apps.messaging.routing.websocket_urlpatterns)
            )
        )
    }
)
