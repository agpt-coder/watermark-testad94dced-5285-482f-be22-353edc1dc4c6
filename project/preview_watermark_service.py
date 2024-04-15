import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class WatermarkSettings(BaseModel):
    """
    Defines the customization options for the watermark to be applied such as type, opacity, position, scale, and rotation.
    """

    type: prisma.enums.WatermarkType
    opacity: float
    position: str
    scale: float
    rotation: float


class PreviewWatermarkResponse(BaseModel):
    """
    Provides a URL pointing to a preview of the watermarked document, enabling the user to review before final application.
    """

    preview_url: str


async def preview_watermark(
    document_id: str, watermark_settings: WatermarkSettings
) -> PreviewWatermarkResponse:
    """
    Generate a preview of the watermarked document.

    Args:
    document_id (str): Identifier for the uploaded PDF document to be watermarked.
    watermark_settings (WatermarkSettings): The settings to be used for the watermark including type, opacity, position, scale, and rotation.

    Returns:
    PreviewWatermarkResponse: Provides a URL pointing to a preview of the watermarked document, enabling the user to review before final application.
    """
    upload = await prisma.models.Upload.prisma().find_unique(where={"id": document_id})
    if not upload:
        return PreviewWatermarkResponse(preview_url="Document not found")
    preview_url = f"https://preview.watermarkservice.com/{document_id}?opacity={watermark_settings.opacity}&position={watermark_settings.position}&scale={watermark_settings.scale}&rotation={watermark_settings.rotation}"
    return PreviewWatermarkResponse(preview_url=preview_url)
