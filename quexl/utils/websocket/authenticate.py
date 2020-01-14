from functools import wraps
from typing import Callable


class Authenticate:
    @staticmethod
    def __call__(func: Callable, **kwargs) -> Callable:
        @wraps(func)
        async def authenticate(self, **kwargs):
            await self.accept()

            if not self.scope["user"].is_authenticated:
                await self.send_json({"error": self.scope["error"]})
                await self.close()
                return

            return await func(self, **kwargs)

        return authenticate
