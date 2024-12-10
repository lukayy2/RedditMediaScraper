from dataclasses import dataclass

from src.data.Media import Media
from src.enum.TypeEnum import TypeEnum


@dataclass
class Post:
    Type: TypeEnum
    ID: str
    PostCollectionName: str  # subreddit or user/author
    Title: str
    IsLink: bool
    IsPinned: bool
    UpVotes: int
    DownVotes: int
    CreatedAtUTC: int
    arrMedia: list[Media]
