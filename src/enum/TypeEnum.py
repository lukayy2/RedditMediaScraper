from enum import Enum


class TypeEnum(Enum):
    SubReddit = 'subreddit'
    User = 'user'

    def __str__(self):
        return self.value
