from dataclasses import dataclass

from m3u8.model import Playlist


@dataclass
class RatedPlaylist:
    intVideoQuality: int
    intAudioQuality: int
    objPlaylist: Playlist
