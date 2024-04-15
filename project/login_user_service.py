import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    Contains limited user-specific information returned upon successful authentication.
    """

    user_id: str
    user_email: str
    user_role: str


class UserLoginResponse(BaseModel):
    """
    Provides feedback on the outcome of the login attempt, including a session token upon successful authentication.
    """

    session_token: str
    user_info: UserInfo


async def login_user(email: str, password: str) -> UserLoginResponse:
    """
    Authenticate user and create a session.

    Args:
    email (str): The email address of the user attempting to log in.
    password (str): The password for the account, to be verified against the stored hash.

    Returns:
    UserLoginResponse: Provides feedback on the outcome of the login attempt, including a session token upon successful authentication.

    Raises:
    Exception: With message "Incorrect email or password" if authentication fails.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and bcrypt.checkpw(
        password.encode("utf-8"), user.hashedPassword.encode("utf-8")
    ):
        session_token = "fake_session_token_for_demo_purpose"
        user_info = UserInfo(
            user_id=user.id, user_email=user.email, user_role=user.role
        )
        return UserLoginResponse(session_token=session_token, user_info=user_info)
    else:
        raise Exception("Incorrect email or password")
