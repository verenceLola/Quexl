from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import quexl.apps.messaging.routing
from quexl.apps.messaging.middlewares import JWTAuthMiddlewareStack

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
