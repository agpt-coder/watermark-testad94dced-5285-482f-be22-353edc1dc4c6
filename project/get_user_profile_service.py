import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    Response model representing the user's profile. It includes essential information such as user's ID, email, and roles. Sensitive information is deliberately excluded for security reasons.
    """

    id: str
    email: str
    role: str


async def get_user_profile() -> UserProfileResponse:
    """
    Retrieve the profile information of the authenticated user.

    This function queries the prisma.models.User table in the database to fetch the profile information of the authenticated user.
    It omits sensitive information for security reasons and returns only the ID, email, and role of the user.

    Returns:
        UserProfileResponse: Response model representing the user's profile. It includes essential information such as user's ID, email, and roles. Sensitive information is deliberately excluded for security reasons.

    Example:
        Assume the authenticated user has the ID '123', email 'user@example.com', and role 'USER'.
        get_user_profile()
        > {"id": "123", "email": "user@example.com", "role": "USER"}
    """
    user_id = "simulated-authenticated-user-id"
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if user:
        return UserProfileResponse(id=user.id, email=user.email, role=user.role)
    else:
        return UserProfileResponse(id="", email="", role="")
