from random import random
from time import time

import numpy


class PushID(object):
    """
    A class that implements firebase's fancy ID generator that creates
    20-character string identifiers with the following properties:
    1. They're based on timestamp so that they sort *after* any existing ids.
    2. They contain 72-bits of random data after the timestamp so that IDs
       won't collide with other clients' IDs.
    3. They sort *lexicographically* (so the timestamp is converted to
       characters that will sort properly).
    4. They're monotonically increasing.  Even if you generate more than one
       in the same timestamp, the latter ones will sort after the former ones.
       We do this by using the previous random bits but "incrementing" them by
       1 (only in the case of a timestamp collision).
    """

    # Modeled after base64 web-safe chars, but ordered by ASCII.
    PUSH_CHARS = (
        "-0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "_abcdefghijklmnopqrstuvwxyz"
    )

    def __init__(self) -> None:
        self.last_push_time = 0
        self.last_rand_chars = numpy.empty(12, dtype=int)

    def next_id(self) -> str:
        """Generates a unique_id.

        Returns:
            unique_id (string): String of length 12.
        """

        now = int(time() * 1000)
        duplicate_time = now == self.last_push_time
        self.last_push_time = now

        unique_id = self.get_unique_id(now)

        self.set_last_rand_char(duplicate_time)

        for i in range(12):
            unique_id += self.PUSH_CHARS[self.last_rand_chars[i]]

        return unique_id

    def get_unique_id(self, now: int) -> str:
        """Creates a unique id which is of length 8.

        Args:
            now (int): Current time converted to integer type.
        Returns:
            unique_id (string): String of length 8.
        """

        time_stamp_chars = numpy.empty(8, dtype=str)

        for i in range(7, -1, -1):
            time_stamp_chars[i] = self.PUSH_CHARS[now % 64]
            now = int(now / 64)

        unique_id = "".join(time_stamp_chars)

        return unique_id

    def set_last_rand_char(self, duplicate_time: bool) -> None:
        """Updates the last random characters.

        Args:
            duplicate_time (bool): Boolean value if time is duplicate.
        """
        if not duplicate_time:
            for i in range(12):
                self.last_rand_chars[i] = int(random() * 64)
        else:
            self.get_previous_rand_char()

    def get_previous_rand_char(self):
        """Updates the last random characters if time is duplicate."""

        for i in range(11, -1, -1):
            if self.last_rand_chars[i] == 63:
                self.last_rand_chars[i] = 0
            else:
                break
        self.last_rand_chars[i] += 1
