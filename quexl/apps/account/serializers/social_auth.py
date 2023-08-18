from rest_framework import serializers


class SocialAuthSerializer(serializers.Serializer):
    """Accepts provider, access token , and access_token_secret"""

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True
    )
    access_token_secret = serializers.CharField(
        max_length=4096, required=False, trim_whitespace=True
    )
