import os
import uuid
from typing import Tuple
from livekit import api as lk
from .config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET

def mint_join_token(
    room: str,
    identity: str | None = None,
    name: str | None = None,
    can_publish: bool = True,
    can_subscribe: bool = True,
) -> Tuple[str, str]:
    """
    Create a LiveKit room-join token (JWT) for a participant.
    Returns (token, identity).
    """
    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        raise RuntimeError("LIVEKIT_API_KEY / LIVEKIT_API_SECRET are not set")

    pid = identity or uuid.uuid4().hex[:12]
    pname = name or pid

    token = (
        lk.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(pid)
        .with_name(pname)
        .with_grants(
            lk.VideoGrants(
                room_join=True,
                room=room,
                can_publish=can_publish,
                can_subscribe=can_subscribe,
            )
        )
        .to_jwt()
    )

    return token, pid
