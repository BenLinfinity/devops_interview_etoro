# Book Fetcher Script

A Python script which fetches a Book from the Open Library API based on A users input keyword and filters it according to author name, release year/release year range or no filter. The script then formats and validates the data using Pydantic models and saves the output as a JSON file according to the users selected path.

**Requirements:** requests version 2.33.1, pydantic version 2.13.2.

**Files:**
- Main.py: the Main script logic
- DataFilter: A module for the purpose of filtering data based on the users selection
- FormatClass: A module containing an abstract base class acting as a standard interface for output formatting functions and a JSON formatting function which uses that class.
- PydanticClass: A module containing Pydantic model definitions to structure and validate output into relevant fields.

**Implementation:** 
- I first researched about pydantic models and their role in the task.
- Then, I planned the functions I would need and the flow of the script deciding to first take user input as a basis and then have the user choose a filter.
- After this, I started implementing the core logic including the Pydantic models with the necessarry fields, and the API call.
- Later, I implemented the filter logic based on user selection using a modular approach of a single filter_logic function in main which then calls functions in a different modules based on user input, I decided on this approach to allow clearly adding other fields in the future.
- Finally, I defined an interface to format the data ensuring future implemented functions would use a specific structure based on an abstract base class and a function which formats to JSON as required. I made sure to separate the logic of saving formatting and saving the data to a file to allow easily using the data for different purposes in the future.
- After the script was fully functional I added error handling for a smooth experience, docstrings and comments for clarity and documentation and input validation to catch improper function/user inputs early.