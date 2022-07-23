from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_invite():
    return "invite app created!"
