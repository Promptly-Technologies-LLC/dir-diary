# dir_diary\mapper.py
2023-09-12 20:59:27
Pseudocode Summary:

1. Import the necessary modules and classes: os, pathspec, Path, datetime, and ProjectFile from file_handler.
2. Define a function called "map_project_folder" that takes an optional argument "startpath" and returns a list of ProjectFile objects.
3. Convert the "startpath" argument to a Path object.
4. Initialize an empty list called "paths_and_modifications" to store the paths and modifications.
5. Walk the directory tree starting from the "startpath".
6. For each file in the directory, create a ProjectFile object with the relative file path and modified time, and append it to the "paths_and_modifications" list.
7. Return the "paths_and_modifications" list.
8. Define a function called "remove_gitignored_files" that takes two optional arguments: "startpath" and "project_files" (default value is a ProjectFile object representing the .gitignore file).
9. Convert the "startpath" argument to a Path object.
10. Get a list of all .gitignore files in the "project_files" list.
11. Create a copy of the "project_files" list and store it in a variable called "filtered_files".
12. Remove files with a parent .git folder from the "filtered_files" list.
13. Iterate over the .gitignore files.
14. Get the directory containing the .gitignore file.
15. Read the lines of the .gitignore file.
16. Create a pathspec object for the .gitignore file.
17. Get the subset of "filtered_files" that are in the same directory tree as the .gitignore file.
18. Get the subset of "same_dir_files" that match the pathspec.
19. Remove the matching files from the "filtered_files" list.
20. Return the "filtered_files" list.
21. If the script is being run directly, import the "map_project_folder" function from the "dir_diary.mapper" module.
22. Call the "map_project_folder" function with the "startpath" argument set to "." and store the result in a variable called "paths_list".
23. Iterate over the "paths_list" and print the "path" and "modified" attributes of each entry.

# dir_diary\client.py
2023-09-15 18:06:26
Pseudocode Summary:

1. Import the `validate_temperature` and `validate_api_key` functions from the `validators` module.
2. Import the `load_dotenv` function from the `dotenv` module.
3. Import the `getenv` function from the `os` module.
4. Import the `Optional` and `Union` types from the `typing` module.

5. Define a class called `LLMClient` with class attributes `_instance` and `_initialized`.

6. Define a `__new__` method that checks if the `_instance` attribute is `None`, and if so, creates a new instance of the `LLMClient` class. Otherwise, it returns the existing instance.

7. Define an `__init__` method that takes in several optional and required arguments. If the `_initialized` attribute is `True`, exit the method.

8. If no `api_key` argument is provided, load the API key from the .env file or environment using the `load_dotenv` and `getenv` functions.

9. Assign the validated `api_key` to the `self.api_key` attribute.

10. Assign the provided `model_name` argument to the `self.model_name` attribute.

11. Assign the provided `long_context_fallback` argument to the `self.long_context_fallback` attribute.

12. Validate the `temperature` argument using the `validate_temperature` function and assign it to the `self.temperature` attribute.

13. If no `total_cost` argument is provided, assign `0` to the `self.total_cost` attribute. Otherwise, assign the validated `total_cost` argument to the `self.total_cost` attribute.

14. Set the `_initialized` attribute to `True` to indicate that the initialization process is complete.

# dir_diary\openai_chatbot.py
2023-09-16 16:01:03
This code defines functions and prompts for working with a language model chatbot to generate summaries and usage instructions for code modules. The main functions and prompts are as follows:

- `classify_project_files_by_role`: This function takes a `project_map` of files and uses the chatbot to classify each file by its role in a software project. It converts the `project_map` to an input string, queries the chatbot with the input string and pre-defined functions, and returns the classified `parsed_project_map`.

- `summarize_with_openai`: This function generates an abbreviated natural-language summary of a code module. It takes an `input_str` (the code module) and a `summary_type` ("pseudocode" or "usage"). Based on the `summary_type`, it selects the appropriate prompt and queries the chatbot for a summary. It then returns the generated summary.

- `get_max_tokens`: This function determines the maximum number of tokens to use for querying the chatbot based on the `long` argument and the client's configuration. It initializes an `LLMClient` object, sets the `model_name` based on the configuration and `long` argument, and sets the `max_tokens` based on the `model_name`. It returns the `max_tokens`.

- `query_llm`: This function queries the chatbot using a prompt and optional functions. It initializes an `LLMClient` object and sets the API key. It prepares the common arguments for the query, including the prompt, model name, and max tokens. If functions are provided, it includes them in the `request_args`. It then generates the output from the input using the OpenAI API. If an error occurs, it tries again with the `long_context_fallback` if available. It updates the total cost and returns the response object.

- `calculate_cost`: This function calculates the cost of a query based on the response from the chatbot. It retrieves the prompt and completion tokens count from the response, as well as the model used. It gets the cost per token for the model from the `models` object and parses it. It calculates the total cost and returns it.

- `parse_and_calculate`: This helper function parses and calculates a cost string in the form "numerator / denominator". It splits the string and converts the numerator and denominator to floating-point numbers. It calculates and returns the result.

# dir_diary\classifier.py
2023-09-16 16:25:57
Abbreviated pseudocode summary:

Imported objects:
- Path from pathlib
- json

Function: initialize_project_map(project_map_path)
- Arguments: project_map_path (Path)
- Returns: project_map (FileClassificationList)

    - Initialize project_map as an empty FileClassificationList
    - If the project_map_file exists:
        - If the project_map_file is empty:
            - Print a warning and return the empty project_map
        - Open the project_map_file as a JSON file and load it as a list of dictionaries
        - Validate the project_map_json and assign it to project_map
    - Return the project_map

Function: update_project_map(project_map, project_files)
- Arguments: project_map (FileClassificationList), project_files (list[ProjectFile])
- Returns: updated_project_map (FileClassificationList)

    - Create a list of existing paths in project_map for easier lookup
    - For each file in project_files:
        - If the file's path is not in the existing_paths list:
            - Append a new FileClassification with the file's path and None role to project_map
    - Remove any FileClassification in project_map that has a path not present in project_files
    - Return the updated project_map

Function: classify_files(project_map_file, project_files)
- Arguments: project_map_file (Path), project_files (list[ProjectFile])
- Returns: updated_project_files (list[ProjectFile])

    - Get the project_map by calling the initialize_project_map function with project_map_file as argument
    - Update the project_map by calling the update_project_map function with project_map and project_files as arguments and assign the result back to project_map
    - If there is no FileClassification in project_map that has a None role:
        - Assign roles to project_files based on corresponding roles in project_map
        - Return the updated project_files
    - Update the project_map by calling the classify_with_openai function with project_map as argument and assign the result back to project_map
    - If project_map is not empty:
        - Create the parent directory of project_map_file if it doesn't exist
        - Open project_map_file in write mode and write the JSON-formatted project_map to it
    - Assign roles to project_files based on corresponding roles in project_map
    - Return the updated project_files

Function: assign_roles(project_map, project_files)
- Arguments: project_map (FileClassificationList), project_files (list[ProjectFile])
- Returns: updated_project_files (list[ProjectFile])

    - Create a mapping dictionary of project_files entries to project_map roles by path
    - For each file in project_files:
        - Assign the corresponding role from the mapping dictionary to the file's role attribute
    - Return the updated project_files

# dir_diary\cli.py
2023-09-15 14:31:43
- Import the `summarize_project_folder` function from the `summarize` module.
- Import the `click` module.
- Define a command-line interface command using the `click.command()` decorator.
- Define several command-line options using the `click.option()` decorator:
  - `startpath`: Path to the project folder.
  - `destination`: Destination folder for the generated files.
  - `include`: Types of files to include.
  - `summary_types`: Types of summaries to generate.
  - `api_key`: API key for OpenAI.
  - `model_name`: Name of the OpenAI model.
  - `long_context_fallback`: Fallback model for long context.
  - `temperature`: Temperature for the OpenAI model.
- Define the `cli` function which serves as the command-line interface entry point:
  - Set the function arguments with their corresponding types.
  - Set the function return type.
  - Add a docstring for the function.
  - Call the `summarize_project_folder` function with the provided arguments.
- Call the `cli` function.

# dir_diary\datastructures.py
2023-09-16 13:16:39
Import the necessary libraries:
- From the `typing` module, import `Optional` and `Literal`.
- From the `pathlib` module, import `Path`.
- From the `datetime` module, import `datetime`.
- From the `pydantic` module, import `BaseModel` and `Field`.
- Import the `json` library.

Define the following sets:
- `ALLOWED_SUMMARY_TYPES` with values "pseudocode", "usage", and "tech stack".
- `ALLOWED_ROLES` with values "source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", and "specialized".
- `ALLOWED_MODELS` with values "gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", and "gpt-4-0613".
- `ALLOWED_FALLBACKS` with values "gpt-4", "gpt-4-0314", "gpt-4-0613", "gpt-3.5-turbo-16k", and "gpt-3.5-turbo-16k-0613".

Define the `ProjectFile` class with the following attributes:
- `path` of type `Path`.
- `modified` of type `datetime`.
- `role` of type `Optional` with allowed values of "source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", and "specialized". The default value is `None` and the description is "role the file plays in the project".

Define the `FileClassification` class with the following attributes:
- `path` of type `Path` with the description "file path relative to the project root".
- `role` of type `Optional` with allowed values of "source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", and "specialized". The default value is `None` and the description is "role the file plays in the project".

Define the `FileClassificationList` class with the following attribute:
- `files` of type `list` containing elements of type `FileClassification` with the description "List of file classifications".

Define the `to_json` method within the `FileClassificationList` class that converts a `FileClassificationList` to a JSON-formatted string. This method performs the following steps:
- Convert the `FileClassificationList` to a dictionary using the `model_dump` method with `exclude_unset=True`.
- Iterate over each file in the `files` list and convert the `path` attribute to a string.
- Convert the dictionary to a JSON string using the `json.dumps` method.
- Return the JSON string.

Define the `ModuleSummary` class with the following attributes:
- `path` of type `Path`.
- `modified` of type `datetime`.
- `content` of type `str`.

# dir_diary\file_handler.py
2023-09-14 15:48:05
Pseudocode:

Function: read_summary_file(summary_file)
    Initialize an empty list called summaries
    Try the following:
        If the summary_file does not exist:
            Create the file and return an empty list
        Read the contents of the summary file
        If the content does not contain any sections:
            Log a warning and return an empty list
        Loop through each section in the file
            Split the section into individual lines
            If the section has less than 3 lines, skip it
            Parse and type-hint the parts of the section
            Create a ModuleSummary object with the parsed parts
            Add the ModuleSummary object to the summaries list
    If an exception occurs:
        Log a warning
        Delete the file if it exists
        Create a new empty file
        Return an empty list
    Return the list of ModuleSummary objects

Function: write_summary_file(summaries, summary_file)
    Create an empty string called contents
    For each ModuleSummary object in the summaries list:
        Add a section to the contents string
        Add the path as a header
        Add the modified timestamp
        Add the content
    If summaries is not empty:
        Create the parent directory of the summary_file if it doesn't exist
        Write the contents string to the summary_file

Function: identify_new_and_modified_files(summaries, project_files)
    Create a mapping of 'path' to 'modified' from the summaries list
    Initialize empty lists called new_files and modified_files
    For each ProjectFile object in the project_files list:
        If the path is not in the summaries map, add the file to new_files
        If the file's 'modified' time is later than in the summaries file, add the file to modified_files
    Return the new_files and modified_files lists

Function: remove_deleted_files_from_summaries(summaries, files)
    Convert the 'files' list into a set of paths called file_paths
    Filter the 'summaries' list to include only files present in 'files'
    Return the filtered_summaries list

# dir_diary\summarize.py
2023-09-16 16:30:48
The code is importing various objects and functions from different modules. It defines a function called "summarize_project_folder" that takes several arguments. The function starts by validating the values of certain arguments using a validator function. It then validates the path arguments and initializes an LLMClient object. Next, the function maps the project folder and removes files listed in .gitignore. It then classifies the project files by role and filters them based on the include list. 

The function then starts a loop to generate summaries for each summary type in the summary_types argument. It reads or creates the summary file and gets a list of ModuleSummary objects. It removes any files that have been deleted from the summaries. It identifies new and modified files since the last summary and selects files to summarize. If there are no files to summarize and the updated summaries are identical to the existing summaries, the function exits.

For each file to summarize, the function queries a chatbot for an updated summary. It drops any existing summaries for the file and adds the generated summary to the updated summaries list. Finally, the function writes the updated summaries to the summary file and prints the total cost of the workflow run.

# dir_diary\summarizer.py
2023-09-16 16:18:39
- Import the following objects: Literal from the typing module, ModuleSummary and ProjectFile from the file_handler module, and summarize_with_openai from the openai_chatbot module.
- Define a function called `summarize_file` that takes two arguments: `file_to_summarize` of type ProjectFile and `summary_type` of type Literal with possible values "pseudocode" or "usage". This function returns a ModuleSummary object.
- Open the file specified by `file_to_summarize.path` for reading and assign the content to `input_str`.
- Call the `summarize_with_openai` function with `input_str` and `summary_type` as arguments and assign the output to `generated_summary`.
- Remove hashtags from `generated_summary` and wrap the lines starting with hashtags with double asterisks using the `replace_hashtags` function.
- Create a ModuleSummary object called `module_summary` with the path, modified date, and content from `file_to_summarize` and `generated_summary`.
- Return `module_summary`.

---

- Define a function called `replace_hashtags` that takes a string argument `text` and returns a string.
- Split `text` by newline character and iterate over each line.
- If a line starts with "#", remove the hashtag, strip leading whitespace, and wrap the line with double asterisks.
- Join the modified lines with newline character and return the result.

# dir_diary\validators.py
2023-09-15 14:04:24
Pseudocode Summary:

```
Imported Libraries:
- from typing: Union
- from os: PathLike, access, R_OK, W_OK
- from pathlib: Path
- from contextlib: contextmanager
- import sys
- import openai

Function Definitions:
- disable_exception_traceback():  # Raise exception without printing traceback
    - save current tracebacklimit as default_value
    - set tracebacklimit to 0
        - yield
    - set tracebacklimit to default_value

- validate_literal(value, allowed_set, var_name):  # Generic validation function
    - if value is not in allowed_set:
        - raise ValueError with message

- validate_literals(arguments):  # Function to validate multiple arguments
    - for each arg in arguments:
        - get var_name, allowed_set, and value from arg
        - if value is a list or tuple:
            - for each val in value:
                - call validate_literal with val, allowed_set, and var_name
        - else:
            - call validate_literal with value, allowed_set, and var_name

- validate_paths(startpath, destination):  # Function to validate a path
    - if startpath is not a string or PathLike:
        - raise TypeError with message
    - if destination is not a string or PathLike:
        - raise TypeError with message
    - convert startpath to Path object
    - create destination as startpath concatenated with Path object
    - if startpath doesn't have read permission:
        - raise PermissionError with message
    - if destination doesn't have write permission:
        - raise PermissionError with message
    - return startpath and destination as a tuple

- validate_temperature(temperature):  # Function to validate a temperature value
    - try to convert temperature to a float
        - if it raises a ValueError:
            - raise ValueError with message
    - if float_temperature is an integer:
        - return float_temperature as an int
    - if float_temperature is not between 0 and 1:
        - raise ValueError with message
    - return float_temperature as a float

- validate_api_key(api_key):  # Function to validate an API key
    - try to list models using api_key
        - if it raises an OpenAIError:
            - disable traceback printing temporarily
            - raise the OpenAIError
    - print "Authentication was successful"
    - return api_key
```

# dir_diary\__init__.py
2023-09-13 16:53:55
The code provides an __init__.py file that imports functions and objects from other modules. The imported items are: 
- "summarize_project_folder" function from the "summarize" module 
- "read_summary_file" function and "ModuleSummary" object from the "file_handler" module.

Overall, the purpose of this code is to make these imported items accessible to other modules by including them in the "__all__" list.

