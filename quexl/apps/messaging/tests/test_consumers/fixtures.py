class DMMessageFixtures:
    """
    define various fixtures for testing DMChatConsumer
    """

    msg_response1 = {
        "message": {
            "chatId": 1,
            "text": "hello user2!",
            "sent_at": "2019-10-01T00:00:00Z",
            "sender": {"username": "user1", "email": "user1@quexl.com"},
        }
    }
    msg_response2 = {
        "message": {
            "chatId": 1,
            "text": "I'm fine user1",
            "sent_at": "2019-10-01T00:00:00Z",
            "sender": {"username": "user2", "email": "user2@quexl.com"},
        }
    }
