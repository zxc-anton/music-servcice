from src.apps.profile.main import router
from src.apps.profile.schema import NewEmail, NewPassword
from src.apps.profile.service import ProfileService
from fastapi import Depends
from src.dependency import current_user

@router.get("/")
async def get_user_profile(user: current_user):
    return user

@router.patch("/email")
async def update_email(user: current_user, 
                       email: NewEmail, 
                       service: ProfileService = Depends(ProfileService),
                       ):
    await service.update_email(user.data.ID, email.email)

@router.patch("/password")
async def update_password(
    user: current_user,
    password: NewPassword,
    service: ProfileService = Depends(ProfileService),
):
    await service.update_password(user.data.ID, password)