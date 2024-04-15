from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Confirms the updated fields of the user's profile, except for password.
    """

    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    update_status: str


async def update_user_profile(
    email: Optional[str],
    password: Optional[str],
    name: Optional[str],
    avatar_url: Optional[str],
    bio: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Attempts to update user profile information in the database, handling optional update fields gracefully.

    Args:
        email (Optional[str]): The user's other (new) email to update to.
        password (Optional[str]): The user's new password (expected to be already hashed before calling).
        name (Optional[str]): The user's new name to update to.
        avatar_url (Optional[str]): The new avatar URL for the user.
        bio (Optional[str]): The new biography or description for the user.

    Returns:
        UpdateUserProfileResponse: An object containing the update status, and any fields that were updated.
    """
    user_id = "user_id_placeholder"
    update_data = {}
    if email:
        update_data["email"] = email
    if name:
        update_data["name"] = name
    if avatar_url:
        update_data["avatar_url"] = avatar_url
    if bio:
        update_data["bio"] = bio
    try:
        updated_user = await prisma.models.User.prisma().update(
            where={"id": user_id}, data=update_data
        )
        return UpdateUserProfileResponse(
            email=email,
            name=name,
            avatar_url=avatar_url,
            bio=bio,
            update_status="success",
        )
    except Exception as e:
        return UpdateUserProfileResponse(update_status="failed")
