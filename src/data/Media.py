from dataclasses import dataclass

from src.enum.MediaEnum import MediaEnum


@dataclass
class Media:
    Url: str
    MediaType: MediaEnum