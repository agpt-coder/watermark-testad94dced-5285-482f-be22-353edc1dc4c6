from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Guide(BaseModel):
    """
    Represents a Guide with title, description, and a URL to access the full content.
    """

    title: str
    description: str
    url: str


class Tutorial(BaseModel):
    """
    Defines a Tutorial resource, including video or written tutorials.
    """

    title: str
    description: str
    url: str


class FAQ(BaseModel):
    """
    Represents a frequently asked question.
    """

    question: str
    answer: str


class GetResourcesResponse(BaseModel):
    """
    Contains a list of support materials available to the user. It includes guides, tutorials, and FAQs.
    """

    guides: List[Guide]
    tutorials: List[Tutorial]
    faqs: List[FAQ]


async def get_resources() -> GetResourcesResponse:
    """
    Fetches support materials such as FAQs and tutorials for user access.

    Args:

    Returns:
    GetResourcesResponse: Contains a list of support materials available to the user. It includes guides, tutorials, and FAQs.
    """
    legal_resources = await prisma.models.LegalResource.prisma().find_many()
    guides = [
        Guide(title=res.title, description=res.content, url=res.link or "")
        for res in legal_resources
        if "guide" in res.title.lower()
    ]
    tutorials = [
        Tutorial(title=res.title, description=res.content, url=res.link or "")
        for res in legal_resources
        if "tutorial" in res.title.lower()
    ]
    faqs = [
        FAQ(question=res.title, answer=res.content)
        for res in legal_resources
        if "faq" in res.title.lower()
    ]
    response = GetResourcesResponse(guides=guides, tutorials=tutorials, faqs=faqs)
    return response
