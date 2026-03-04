from fastapi import Depends, HTTPException
from src.apps import user
from src.apps.profile.manager import ProfileManager
from src.apps.auth.handlers import Password_Handlers
from src.apps.profile.schema import NewPassword


class ProfileService:
    def __init__(self, 
                 manager: ProfileManager = Depends(ProfileManager),
                 password_handler: Password_Handlers = Depends(Password_Handlers),
                 ) -> None:
        self.manager: ProfileManager = manager
        self.password_handler = password_handler

    async def update_password(self, id: int, password: NewPassword) -> None: 
        user_password = await self.manager.get_user_passwords(id)
        password_hash = await self.password_handler.get_hashed_password(password.new_password)
        if user_password is None or user_password == "":
            await self.manager.update_fields(id, password_hash=password_hash)
            return
        if not (await self.password_handler.compare_passwords(password.old_password, user_password)):
            raise HTTPException(403)
        await self.manager.update_fields(id, password_hash=password_hash)

    async def update_email(self, id: int, email: str) -> None:
        await self.manager.update_fields(id, email=email)
