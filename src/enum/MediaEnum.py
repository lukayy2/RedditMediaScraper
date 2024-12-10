from enum import Enum


class MediaEnum(Enum):
    Image = 'image'
    Video = 'video'

    def __str__(self):
        return self.value
