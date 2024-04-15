import prisma
import prisma.models
from pydantic import BaseModel


class DeleteDocumentResponse(BaseModel):
    """
    Provides feedback on the result of the document deletion attempt, including success status and any relevant messages.
    """

    success: bool
    message: str


async def delete_user_document(id: str) -> DeleteDocumentResponse:
    """
    Allows a user to delete a specific document from their uploads as well as associated watermarked PDFs.

    This function handles the deletion of user's document by its unique identifier. It also ensures that
    all related watermarked PDFs generated from this document are removed to maintain data consistency.

    Args:
        id (str): The unique identifier for the document to be deleted.

    Returns:
        DeleteDocumentResponse: Provides feedback on the result of the document deletion attempt, including success status and any relevant messages.

    Example:
        delete_user_document("unique-document-id")
        > DeleteDocumentResponse(success=True, message="Document and related data successfully deleted.")
    """
    document = await prisma.models.Upload.prisma().find_unique(where={"id": id})
    if not document:
        return DeleteDocumentResponse(success=False, message="Document not found.")
    await prisma.models.WatermarkedPDF.prisma().delete_many(
        where={"originalUploadId": id}
    )
    await prisma.models.Upload.prisma().delete(where={"id": id})
    return DeleteDocumentResponse(
        success=True, message="Document and related data successfully deleted."
    )
