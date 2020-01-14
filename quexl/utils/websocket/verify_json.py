import json
from functools import wraps
from json import JSONDecodeError
from typing import Callable


class VerifyJSON:
    """
    verify data is valid JSON data
    """

    @staticmethod
    def __call__(func: Callable) -> Callable:
        @wraps(func)
        async def verify_json(self, **kwargs):
            data = kwargs.get("text_data", "")
            try:
                json_data = json.loads(data)
            except JSONDecodeError:
                return await self.send_json({"error": "Invalid JSON data"})
            return await func(self, json_data)

        return verify_json
