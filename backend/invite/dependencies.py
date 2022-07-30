from fastapi import Depends

from backend.core.database import get_session
from backend.invite.repository import InviteRepository


def get_invite_rep(session=Depends(get_session)):
    return InviteRepository(session)
