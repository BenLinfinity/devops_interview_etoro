"""A module to define a standard output interface structure for the project"""
from abc import ABC, abstractmethod
from PydanticClass import Book
from typing import List
import json



class BaseFormat(ABC):
    """An abstract base class forcing an interface structure"""
    @abstractmethod
    def format(self, books: List[Book]):
        pass

class JSONFormat(BaseFormat):
    """A class to format a list of books into JSON"""
    def format(self, books) -> str:
        """
        Parameters:
        books: List[PydanticClass.Book]
        Return: str: JSON formatted list of books
        """
        return json.dumps([book.model_dump() for book in books], indent=2,ensure_ascii=False)