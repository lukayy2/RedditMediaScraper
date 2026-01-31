from dataclasses import dataclass

from src.enum.MediaEnum import MediaEnum


@dataclass
class Media:
    ID: str
    Url: str
    MediaType: MediaEnum