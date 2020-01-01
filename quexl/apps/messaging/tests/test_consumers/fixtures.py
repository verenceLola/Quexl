class DMMessageFixtures:
    """
    define various fixtures for testing DMChatConsumer
    """

    msg_response1 = {
        "message": {
            "chatId": 6,
            "text": "hello user2!",
            "sent_at": "2019-10-01T00:00:00Z",
            "sender": {"username": "user1", "email": "user1@quexl.com"},
        }
    }
    msg_response2 = {
        "message": {
            "chatId": 6,
            "text": "I'm fine user1",
            "sent_at": "2019-10-01T00:00:00Z",
            "sender": {"username": "user2", "email": "user2@quexl.com"},
        }
    }


class GroupMessageFixtures:
    """
    websocket responses for group messaging
    """

    non_member_response = {
        "error": "Message not sent. You're not a member of this group"
    }
    non_exisiting_group_response = {
        "error": "Message not sent. Group named 'non-existing-group' doesn't exist"
    }
