"""
fixtures of testing messaging views
"""


class ChatGroup:
    """
    fixtures for listing and creating chat groups
    """

    @staticmethod
    def new_user_group(group_name: str, members: list) -> dict:
        """
        data for creating new user group
        """
        return {
            "group_name": group_name,
            "members": [{"username": member.username} for member in members],
        }
