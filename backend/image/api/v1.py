from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_image():
    return "image app created!"
