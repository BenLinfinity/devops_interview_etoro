# Book Fetcher Script

A Python script which fetches a book from the Open Library API based on a user's input keyword and filters the results according to author name, release year/release year range or no filter. The script then formats and validates the data using Pydantic models and saves the output as a JSON file according to the user's selected path.

**Requirements:** 
- requests version 2.33.1
- pydantic version 2.13.2.

**Files:**
- Main.py: the main script logic
- DataFilter.py: A module for the purpose of filtering data based on the user's selection
- FormatClass.py: A module containing an abstract base class acting as a standard interface for output formatting functions and a JSON formatting function which uses that class.
- PydanticClass.py: A module containing Pydantic model definitions to structure and validate output into relevant fields.

**Implementation:** 
- I first researched Pydantic models and their role in the task.
- Then, I planned the functions I would need and the flow of the script, deciding to first prompt the user for a keyword, then a filter choice.
- After this, I started implementing the core logic including the Pydantic models with the necessary fields, and the API call.
- Later, I implemented the filter logic based on user selection using a modular approach of a single filter_logic function in main which then calls functions in a separate module based on user input. I decided on this approach to make adding new filter types straightforward in the future.
- Finally, I defined an interface to format the data ensuring future implemented functions would use a specific structure based on an abstract base class and a function which formats to JSON as required. I made sure to separate the logic of saving and formatting the data to a file to allow easily using it for different purposes in the future.
- After the script was fully functional, I added error handling for a smooth experience, docstrings and comments for clarity and input validation to catch improper function/user inputs early.