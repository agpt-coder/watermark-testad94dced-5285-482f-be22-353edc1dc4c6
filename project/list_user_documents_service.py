from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class DocumentDetail(BaseModel):
    """
    Details of a single document uploaded by the user.
    """

    id: str
    fileName: str
    fileType: str
    fileSize: int
    createdAt: str
    path: str


class ListUserDocumentsResponse(BaseModel):
    """
    Response model for listing all documents uploaded by the user. It includes details such as file name, type, size, and the upload timestamp.
    """

    documents: List[DocumentDetail]


async def list_user_documents() -> ListUserDocumentsResponse:
    """
    Lists all documents uploaded by the user.

    Args:


    Returns:
    ListUserDocumentsResponse: Response model for listing all documents uploaded by the user. It includes details such as file name, type, size, and the upload timestamp.
    """
    uploads = await prisma.models.Upload.prisma().find_many()
    documents = [
        DocumentDetail(
            id=upload.id,
            fileName=upload.fileName,
            fileType=upload.fileType,
            fileSize=upload.fileSize,
            createdAt=str(upload.createdAt),
            path=upload.path,
        )
        for upload in uploads
    ]
    return ListUserDocumentsResponse(documents=documents)
