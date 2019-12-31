from functools import wraps

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


class WebSocketUserExists:
    """
    ensure websocket user being sent message exists
    """

    @staticmethod
    def __call__(func):
        @wraps(func)
        async def user_exists(*args, **kwargs):
            self, json_data = args
            self.to = json_data.get("to")

            if self.to.lower() == self.scope["user"].username.lower():
                await self.send_json({"error": "You can't chat with yourself"})

                return

            try:
                self.to = await database_sync_to_async(
                    get_user_model().objects.get
                )(username=self.to)
            except get_user_model().DoesNotExist:
                await self.send_json(
                    {"error": f"user with username '{self.to}' does not exist"}
                )

                return

            return await func(*args, **kwargs)

        return user_exists
