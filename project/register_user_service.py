from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    This model communicates the result of the registration process. It confirms the successful creation of a new user account.
    """

    user_id: str
    email: Optional[str] = None
    registered_via_oauth: bool
    message: str


async def register_user(
    email: Optional[str], password: Optional[str], oauth_token: Optional[str]
) -> RegisterUserResponse:
    """
    Register a new user with email and password or OAuth.

    Args:
    email (Optional[str]): The user's email address. Required for email/password registration.
    password (Optional[str]): The user's chosen password. Required for email/password registration.
    oauth_token (Optional[str]): An OAuth token provided by an external authentication provider. Required for OAuth registration.

    Returns:
    RegisterUserResponse: This model communicates the result of the registration process. It confirms the successful creation of a new user account.

    """
    if oauth_token:
        user = await prisma.models.User.prisma().create(
            data={"email": email, "hashedPassword": ""}
        )
        return RegisterUserResponse(
            user_id=user.id,
            email=email,
            registered_via_oauth=True,
            message="User registered successfully via OAuth.",
        )
    else:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = await prisma.models.User.prisma().create(
            data={"email": email, "hashedPassword": hashed_password.decode("utf-8")}
        )
        return RegisterUserResponse(
            user_id=user.id,
            email=email,
            registered_via_oauth=False,
            message="User registered successfully with email and password.",
        )
