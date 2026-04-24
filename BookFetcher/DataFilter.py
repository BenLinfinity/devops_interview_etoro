"""A module for the purpose of filtering data based on specific criteria"""
from PydanticClass import Book
from typing import List

def filter_data_by_author(author: str,data: List[Book]) -> List[Book]:
    """
    Parameters:
    author(str): author of the book
    data(List[Book]): list of books to filter by author
    Returns:
    List[Book]: list of filtered books
    """
    if author == "":
        raise RuntimeError(f"Author name cannot be empty!")
    result = []
    cleaned_input_author = clean_input(author)
    result = [
        book for book in data
        if book.author_name and any(
            cleaned_input_author in clean_input(name)
            for name in book.author_name)
    ]
    return result

def filter_data_by_year(year_range: tuple[int, int],data: List[Book]) -> List[Book]:
    """
    Parameters:
    year_range(str): range of years
    data(List[Book]): list of books to filter by year range
    Returns:
    List[Book]: list of filtered books
    """
    start_year = min(year_range[0], year_range[1])
    end_year = max(year_range[0], year_range[1])

    result = [
        book for book in data
        if book.first_publish_year
        and start_year <= book.first_publish_year <= end_year
    ]
    return result


def get_year_range(year: str) -> tuple[int, int]:
    """
    Parameters:
    year(str): a single year or range of years separated by "-"
    Returns:
    int: start year, int: end year
    """
    try:
        if "-" in year:
            years = year.split("-", 1)
            first_half = int(years[0].strip())
            second_half = int(years[1].strip())
            return first_half, second_half
        single_year = int(year.strip())
        return single_year, single_year
    except ValueError:
        raise RuntimeError(f"Invalid year format! {year}, use YYYY YYYY-YYYY")

def clean_input(string_input: str) -> str:
    """
    Parameters:
    string_input(): input to be cleaned for versatile matching
    Return:
    str: string with all chars forced to lowercase and special characters removed
    """
    return "".join(char for char in string_input if char.isalnum()).lower()