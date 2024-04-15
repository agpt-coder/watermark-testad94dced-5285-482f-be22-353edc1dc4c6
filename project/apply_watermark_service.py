from typing import Optional

from pydantic import BaseModel


class ApplyWatermarkResponse(BaseModel):
    """
    Confirms the watermark application process and provides the updated document's reference.
    """

    success: bool
    document_id: str
    message: str


class WatermarkType:
    TEXT: str = "TEXT"
    IMAGE: str = "IMAGE"


def apply_watermark(
    document_id: str,
    watermark_type: WatermarkType,
    text_content: Optional[str],
    image_file: Optional[str],
    opacity: float,
    position: str,
    scale: float,
    rotation: float,
) -> ApplyWatermarkResponse:
    """
    Apply the watermark to the selected PDF document.

    ** THIS FUNCTION IS A MOCK IMPLEMENTATION. IN A REAL-WORLD SCENARIO, THIS FUNCTION SHOULD
    INTRODUCE LOGIC TO MODIFY PDF DOCUMENTS BASED ON THE SPECIFIED PARAMETERS. **

    Args:
        document_id (str): The unique identifier of the PDF document to be watermarked.
        watermark_type (WatermarkType): Specifies the type of watermark to apply; could be 'text' or 'image'.
        text_content (Optional[str]): The text content of the watermark. Applicable if watermark_type is 'text'.
        image_file (Optional[str]): The image file of the watermark. Applicable if watermark_type is 'image'.
        opacity (float): The opacity level of the watermark, ranging from 0 to 1.
        position (str): The position of the watermark on the document.
        scale (float): The scale of the watermark relative to the page size.
        rotation (float): The rotation angle of the watermark, in degrees.

    Returns:
        ApplyWatermarkResponse: Confirms the watermark application process and provides the updated document's reference.
    """
    return ApplyWatermarkResponse(
        success=True, document_id=document_id, message="Watermark successfully applied."
    )
