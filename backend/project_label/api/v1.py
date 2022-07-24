from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_project_label():
    return "project_label app created!"
