"""
utility function for generating md5 hash
"""
import hashlib


class MD5:
    """
    calculate md5 for a given object
    """

    @staticmethod
    def __call__(message: str) -> str:
        """
        digest message using md5
        """
        return hashlib.md5(message.encode()).hexdigest()
