"""A module to define pydantic models for the purpose of filtering and validating data fields"""
from pydantic import BaseModel, Field
from typing import List, Optional

class Book(BaseModel):
    """
    A class containing relevant fields to be picked from an API call and used for
    filtering, validation and finally formatting and displaying the data
    """
    title: str
    author_name: List[str] = Field(default_factory=list)
    first_publish_year: Optional[int] = None

class ApiResponse(BaseModel):
    """A class representing a response object from API call with docs being the top level field"""
    docs: List[Book]