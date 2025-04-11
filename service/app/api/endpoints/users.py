from fastapi import APIRouter, Depends

from app import schemas, models
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("", response_model=schemas.UserResponse)
def create_user(
    user_create: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    pass