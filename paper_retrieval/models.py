"""
Pydantic models for paper metadata and API responses.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Author(BaseModel):
    """Author information model."""
    authorId: Optional[str] = None
    name: str


class OpenAccessPdf(BaseModel):
    """Open access PDF information model."""
    url: str
    status: Optional[str] = None


class PaperMetadata(BaseModel):
    """
    Paper metadata model matching Semantic Scholar API response.
    """
    paperId: str
    title: str
    authors: Optional[List[Author]] = None
    year: Optional[int] = None
    abstract: Optional[str] = None
    citationCount: Optional[int] = Field(default=0)
    openAccessPdf: Optional[OpenAccessPdf] = None
    
    class Config:
        populate_by_name = True
        # Pydantic v2 compatibility
        json_encoders = {
            # Handle any special encoding if needed
        }
    
    def has_open_pdf(self) -> bool:
        """Check if paper has an open access PDF available."""
        return self.openAccessPdf is not None and self.openAccessPdf.url is not None
    
    def get_pdf_url(self) -> Optional[str]:
        """Get the open access PDF URL if available."""
        if self.has_open_pdf():
            return self.openAccessPdf.url
        return None


class SemanticScholarSearchResponse(BaseModel):
    """Response model for Semantic Scholar search API."""
    total: Optional[int] = None
    offset: Optional[int] = None
    data: List[PaperMetadata] = []

