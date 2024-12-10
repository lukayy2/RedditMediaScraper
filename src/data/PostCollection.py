from dataclasses import dataclass

from src.data.Post import Post


@dataclass
class PostCollection:
    AfterPointer: str
    BeforePointer: str
    ListPosts: list[Post]