"""
The main module containing the core logic of the script
The script calls the Open Library API based on a keyword provided by a user as prompted input.
It Then filters the output based on author, release year (single or range) or none
and saves the data as a JSON file.
"""
import requests
from typing import List
from pathlib import Path
from pydantic import ValidationError
from enum import Enum

from PydanticClass import ApiResponse, Book
from DataFilter import filter_data_by_year,filter_data_by_author,get_year_range
from FormatClass import JSONFormat

class FilterTypes(Enum):
    PUBLISH_YEAR = "1"
    AUTHOR = "2"
    NONE = "3"
def main():
    """
    Function Description
    receives a keyword as user input,
    makes an api call to search for books based on the keyword and returns it
    """

    print("--------- Book Finder ---------")
    keyword = get_keyword_input()
    filter_type, filter_value = get_filter_input()

    try:
        result = book_fetch(keyword)
    except RuntimeError as e:
        raise SystemExit(e)

    new_data = filter_logic(filter_type,filter_value, result.docs)
    if not new_data:
        raise SystemExit(f"Error! No results found for {keyword} with filter {filter_value}")

    json_data = JSONFormat().format(new_data)

    get_save_path(keyword,json_data)



def get_keyword_input() -> str:
    """
    Prompts the user to enter a keyword and captures it.
    Returns:
    keyword (str): the user's input to be used to find relevant books
    """
    while True:
        keyword = input("Please enter a keyword to search by: ")
        if keyword:
            return keyword
        else:
            print("Please enter a valid keyword to search by: ")

def get_filter_input() -> tuple[FilterTypes, str | tuple[int, int]]:
    """
    Prompts the user to enter filter info and captures it.
    Returns:
    selection (str): a string number representing the type of filter to be made
    filter_value (str | tuple[int, int]): the artist name or the year range as a tuple of 2 integers.
    """
    while True:
        # validates user input immediately by comparing with enum class
        try:
            selection = FilterTypes(input("What data would you like to filter by? Choose by number:\
                         \n1) Publish Year \n2) Author \n3) None\n"))
            break
        except ValueError:
            print("Please choose a valid number \n")


    if selection == FilterTypes.PUBLISH_YEAR:
        filter_value = input("Please enter a year or range of years separated with a \"-\" to filter by: ")
        while True:
            try:
                filter_value = get_year_range(filter_value)
                break
            except RuntimeError as e:
                filter_value = input(f"{e}, Try Again: ")
    elif selection == FilterTypes.AUTHOR:
        filter_value = input("Please enter an Author Name to filter by: ")
    else:
        filter_value = ""

    return selection, filter_value

def get_save_path(keyword,json_data):
    file_path = input("Please enter the directory path to save file to: ")
    while True:
        try:
            save_to_file(json_data, keyword, "json", file_path)
            break
        except RuntimeError as e:
            print(f"Error: {e}\n")

            file_path = input("Please write a valid directory path:")

def book_fetch(keyword: str) -> ApiResponse:
    """
    Parameters:
    keyword (str) : key word to search for in an API call to the Open Library API
    Returns:
    APIResponse: pydantic class object containing the API response in the format docs.List[Book]
    """
    try:
        response =  requests.get("https://openlibrary.org/search.json", params={"q": keyword}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise RuntimeError(f"Error: No results found for {keyword} ")

        return ApiResponse(**data)

    except ValidationError:
        raise RuntimeError("Error! API returned invalid format")
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Please try again later.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"API Error! {e}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Oops! an Error has occured, Please try again later: {e}")



def filter_logic(data_filter: FilterTypes,filter_value: str | tuple[int, int], data: List[Book]) -> List[Book]:
    """
    Parameters:
    data_filter (FilterTypes): API field as an enum class instance to filter by
    filter_value (str): value to filter by
    data (PydanticClass.List[Book]): list of books to be filtered, formatted and saved
    Returns:
    PydanticClass.List[Book]: filtered list of books
    """
    if data_filter == FilterTypes.PUBLISH_YEAR:
        return filter_data_by_year(filter_value, data)
    elif data_filter == FilterTypes.AUTHOR:
        return filter_data_by_author(filter_value, data)
    else:
        return data


def save_to_file(data:str, keyword:str, file_suffix:str, file_path:str) -> None:
    """
    Parameters:
    data (str) data to be saved to a file
    keyword (str): searched keywords to use for file-name
    file_suffix (str): suffix to append to file name
    file_path (str): path to save file provided by user
    """
    # normalizes path allowing ~ and ../
    path = Path(file_path).expanduser().resolve() / f"{keyword}.{file_suffix}"
    # creates parents if they dont exist
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            f.write(data)
    except PermissionError:
        raise RuntimeError("Permission Denied")
    except OSError as e:
        raise RuntimeError(e)



if __name__ == "__main__":
    main()