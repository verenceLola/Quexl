from typing import Dict
from typing import Union
from urllib.parse import parse_qs

from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed

from quexl.apps.account.backends import JWTAuthentication


class MockWebSocketAuth:
    async def connect(self) -> None:
        token = MockWebSocketAuth().get_token(self.scope)
        jwt = JWTAuthentication()
        await self.accept()
        try:
            user, _ = jwt.authenticate_credentials(token)
            self.scope["user"] = user
            await self.send_json({"message": "connection established"})
        except AuthenticationFailed as e:
            await self.send_json({"error": e.detail})
            self.scope["user"] = AnonymousUser
            await self.close()
            return

    @staticmethod
    def get_token(scope: Dict[str, Union[str, bytes, Dict[str, str]]]) -> str:
        """
        get token from headers or query string
        """
        qs = scope["query_string"]
        headers = scope["headers"]
        MockWebSocketAuth().parse_query_string_token(
            query_string=qs, headers=headers
        )
        return MockWebSocketAuth().parse_header_token(headers=headers)

    def parse_header_token(self, headers: Dict[str, str]) -> str:
        """
        parse token in request header
        """
        if "Authorization" in headers:
            token_name, token_value = headers["Authorization"].split()
            if token_name == "Bearer":
                return token_value
        else:
            return ""

    def parse_query_string_token(
        self, query_string: bytes, headers: Dict[str, str]
    ) -> str:
        """
        parse query token in query string and add to header if found
        """
        if b"token" in query_string:
            parsed_query_string = parse_qs(query_string)
            headers.update(
                {"Authorization": parsed_query_string[b"token"][0].decode()}
            )
