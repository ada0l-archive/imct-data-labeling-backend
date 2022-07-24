from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_label_type():
    return "label_type app created!"
