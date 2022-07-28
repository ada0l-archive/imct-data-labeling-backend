from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_label():
    return "label app created!"
