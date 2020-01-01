from functools import wraps

from channels.db import database_sync_to_async

from quexl.apps.messaging.models import Thread


class IsGroupMember:
    @staticmethod
    def __call__(func):
        @wraps(func)
        async def ensure_group_member(self, json_data):
            """
            ensure current user a group member
            """
            self.thread_name = json_data.get("group")
            self.group_name = f"{self.thread_name}"
            try:
                self.thread = await database_sync_to_async(Thread.objects.get)(
                    name=self.group_name
                )
                if not Thread.objects.filter(
                    participants__in=[self.scope["user"]]
                ).exists():
                    await self.send_json(
                        {
                            "error": f"Message not sent. You're not a member"
                            " of this group"
                        }
                    )
                    return
            except Thread.DoesNotExist:
                await self.send_json(
                    {
                        "error": f"Message not sent. Group named"
                        f" '{self.group_name}' doesn't exist"
                    }
                )
                return
            return await func(self, json_data)

        return ensure_group_member
