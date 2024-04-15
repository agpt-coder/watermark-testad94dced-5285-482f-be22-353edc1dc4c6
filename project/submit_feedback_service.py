import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Response model for when a user successfully submits feedback.
    """

    success: bool
    message: str


async def submit_feedback(user_id: str, content: str) -> SubmitFeedbackResponse:
    """
    Allows users to submit feedback directly from the platform.

    Args:
    user_id (str): The ID of the user submitting feedback. This should be extracted from the user's session or token rather than explicitly passed to ensure security.
    content (str): The content of the user's feedback.

    Returns:
    SubmitFeedbackResponse: Response model for when a user successfully submits feedback.
    """
    try:
        await prisma.models.Feedback.prisma().create(
            data={"userId": user_id, "content": content}
        )
        success = True
        message = "Feedback submitted successfully."
    except Exception as e:
        success = False
        message = f"Failed to submit feedback: {str(e)}"
    return SubmitFeedbackResponse(success=success, message=message)
