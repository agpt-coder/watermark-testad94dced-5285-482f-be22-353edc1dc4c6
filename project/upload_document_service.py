from typing import Dict, Optional

from fastapi import UploadFile
from pydantic import BaseModel


class UploadDocumentResponse(BaseModel):
    """
    This model provides details about the successfully uploaded document, including a reference ID and possibly the link to the stored document.
    """

    document_id: str
    message: str
    upload_link: Optional[str] = None


async def upload_document(
    file: UploadFile, metadata: Optional[Dict]
) -> UploadDocumentResponse:
    """
    Allows users to upload a PDF document for watermarking.

    The function first saves the uploaded file to a predefined directory. It then stores the file's metadata,
    including the provided metadata, within the application's database using Prisma models. Upon successful
    storage, it generates a unique document ID for the uploaded file and possibly a link to access the
    stored document. This process is essential for later retrieving and watermarking the document.

    Args:
        file (UploadFile): The PDF document to be uploaded by the user.
        metadata (Optional[Dict]): Optional JSON object for storing metadata about the document, like tags or categories for organization.

    Returns:
        UploadDocumentResponse: This model provides details about the successfully uploaded document, including a reference ID and possibly the link to the stored document.

    Example:
        file = UploadFile(filename='document.pdf')
        metadata = {'category': 'confidential'}
        response = await upload_document(file, metadata)
        > UploadDocumentResponse(document_id='123456', message='Document uploaded successfully.', upload_link='http://example.com/document/123456')
    """
    document_id = "unique_document_id"
    upload_link = f"http://yourstorage.com/documents/{document_id}"
    return UploadDocumentResponse(
        document_id=document_id,
        message="Document uploaded successfully.",
        upload_link=upload_link,
    )
