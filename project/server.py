import logging
from contextlib import asynccontextmanager
from typing import Dict, Optional

import prisma
import prisma.enums
import project.apply_watermark_service
import project.delete_user_document_service
import project.get_resources_service
import project.get_user_profile_service
import project.list_user_documents_service
import project.login_user_service
import project.logout_user_service
import project.preview_watermark_service
import project.register_user_service
import project.submit_feedback_service
import project.update_user_profile_service
import project.upload_document_service
from fastapi import FastAPI, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="watermark-test",
    lifespan=lifespan,
    description="The task involves creating a solution that allows users to add text or image watermarks to PDF files. This solution must offer flexibility and control over the watermark's customization, including its opacity, position, and size, ensuring that the watermark does not obscure the content of the PDF. From the user's perspective, both text and image watermarks are essential for different use cases, with text watermarks being favored for their simplicity in certain contexts, and image watermarks being critical for branding purposes.\n\nThe envisioned interface for this solution includes a web-based platform where users can upload the PDF and the watermark file (whether text or image) through a user-friendly mechanism such as a drag-and-drop area or a file upload button. The platform should support popular image formats for image watermarks and provide clear labeling of each upload section to avoid user confusion. To adjust the watermark settings, a side panel or modal window should allow users to modify parameters like opacity, position, scale, and rotation. A real-time preview feature is also highly desired for users to see the watermark's appearance on the PDF before the finalizing step.\n\nFor the implementation, using Python is recommended due to its robust libraries for PDF manipulation such as PyPDF2 and ReportLab. These libraries can handle the technical requirements needed for implementing the watermarking functionality effectively, including adjusting the opacity of elements, preserving the original document's quality, and ensuring compatibility across various PDF viewers. Best practices include using transparent overlays to maintain document usability, securing the watermarks against removal, and optimizing the performance for batch processing scenarios.\n\nThis solution requires careful consideration of copyright and privacy laws to ensure the practice of watermarking complies with legal standards. Finally, providing detailed customization options allows the tool to cater to a broad range of needs, from simple copyright assertion to complex branding strategies.",
)


@app.get(
    "/user/profile", response_model=project.get_user_profile_service.UserProfileResponse
)
async def api_get_get_user_profile() -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Retrieve the profile information of the authenticated user.
    """
    try:
        res = await project.get_user_profile_service.get_user_profile()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/logout", response_model=project.logout_user_service.LogoutUserResponse)
async def api_post_logout_user(
    session_token: str,
) -> project.logout_user_service.LogoutUserResponse | Response:
    """
    Logout the user and terminate the session.
    """
    try:
        res = await project.logout_user_service.logout_user(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    email: Optional[str],
    password: Optional[str],
    name: Optional[str],
    avatar_url: Optional[str],
    bio: Optional[str],
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Update the user's profile information.
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            email, password, name, avatar_url, bio
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/login", response_model=project.login_user_service.UserLoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.UserLoginResponse | Response:
    """
    Authenticate user and create a session.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/watermark/preview",
    response_model=project.preview_watermark_service.PreviewWatermarkResponse,
)
async def api_get_preview_watermark(
    document_id: str,
    watermark_settings: project.preview_watermark_service.WatermarkSettings,
) -> project.preview_watermark_service.PreviewWatermarkResponse | Response:
    """
    Generate a preview of the watermarked document.
    """
    try:
        res = await project.preview_watermark_service.preview_watermark(
            document_id, watermark_settings
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/resources/get", response_model=project.get_resources_service.GetResourcesResponse
)
async def api_get_get_resources() -> project.get_resources_service.GetResourcesResponse | Response:
    """
    Fetches support materials such as FAQs and tutorials for user access.
    """
    try:
        res = await project.get_resources_service.get_resources()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/watermark/apply",
    response_model=project.apply_watermark_service.ApplyWatermarkResponse,
)
async def api_post_apply_watermark(
    document_id: str,
    watermark_type: prisma.enums.WatermarkType,
    text_content: Optional[str],
    image_file: Optional[str],
    opacity: float,
    position: str,
    scale: float,
    rotation: float,
) -> project.apply_watermark_service.ApplyWatermarkResponse | Response:
    """
    Apply the watermark to the selected PDF document.
    """
    try:
        res = project.apply_watermark_service.apply_watermark(
            document_id,
            watermark_type,
            text_content,
            image_file,
            opacity,
            position,
            scale,
            rotation,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback/submit",
    response_model=project.submit_feedback_service.SubmitFeedbackResponse,
)
async def api_post_submit_feedback(
    user_id: str, content: str
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Allows users to submit feedback directly from the platform.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(user_id, content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/document/upload",
    response_model=project.upload_document_service.UploadDocumentResponse,
)
async def api_post_upload_document(
    file: UploadFile, metadata: Optional[Dict]
) -> project.upload_document_service.UploadDocumentResponse | Response:
    """
    Allows users to upload a PDF document for watermarking.
    """
    try:
        res = await project.upload_document_service.upload_document(file, metadata)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/document/list",
    response_model=project.list_user_documents_service.ListUserDocumentsResponse,
)
async def api_get_list_user_documents() -> project.list_user_documents_service.ListUserDocumentsResponse | Response:
    """
    Lists all documents uploaded by the user.
    """
    try:
        res = await project.list_user_documents_service.list_user_documents()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/document/{id}/delete",
    response_model=project.delete_user_document_service.DeleteDocumentResponse,
)
async def api_delete_delete_user_document(
    id: str,
) -> project.delete_user_document_service.DeleteDocumentResponse | Response:
    """
    Allows a user to delete a specific document.
    """
    try:
        res = await project.delete_user_document_service.delete_user_document(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/register", response_model=project.register_user_service.RegisterUserResponse
)
async def api_post_register_user(
    email: Optional[str], password: Optional[str], oauth_token: Optional[str]
) -> project.register_user_service.RegisterUserResponse | Response:
    """
    Register a new user with email and password or OAuth.
    """
    try:
        res = await project.register_user_service.register_user(
            email, password, oauth_token
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
