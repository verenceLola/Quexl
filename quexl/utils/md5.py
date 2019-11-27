"""
utility function for generating md5 hash
"""
import hashlib


def md5(message: str) -> str:
    """
    digest message using md5
    """
    return hashlib.md5(message.encode()).hexdigest()
