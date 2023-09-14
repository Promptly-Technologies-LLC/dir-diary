# dir_diary\chatbot.py
2023-09-12 00:00:28
1. Import necessary libraries and modules: os, dotenv, typing, langchain.chat_models, langchain, openai.error, langchain.output_parsers, pydantic.BaseModel.
2. Define a function named "initialize_model" with the following arguments:
   - api_key (string, optional)
   - temperature (float, optional)
   - model_name (string, optional)
   - callbacks (list, optional)
   The function returns a ChatOpenAI object.
3. Inside the "initialize_model" function:
   - Check if the api_key argument is None.
   - If api_key is None, load the API key from the .env file or environment.
   - Create a ChatOpenAI object named "llm" using the provided arguments.
   - Return the "llm" object.
4. Define a function named "query_llm" with the following arguments:
   - prompt (PromptTemplate)
   - input_str (string)
   - llm (ChatOpenAI)
   - long_context_llm (ChatOpenAI)
   - parser (PydanticOutputParser, optional)
   The function returns a BaseModel object.
5. Inside the "query_llm" function:
   - Create an LLMChain object named "llm_chain" using the provided arguments.
   - Try to generate the output from the input using the "llm_chain" object.
   - If an InvalidRequestError is raised:
     - Check if "long_context_llm" is None.
     - If "long_context_llm" is None, raise the error.
     - If "long_context_llm" is not None, print a warning message, update the "llm_chain" object with "long_context_llm", and generate the output again.
   - If no parser is provided, return the raw output.
   - If a parser is provided, parse the output using the provided parser.
   - Return the parsed output.

# dir_diary\validators.py
2023-09-13 16:41:57
1. Import the necessary objects and functions from the `typing`, `os`, and `pathlib` modules.

2. Define a function named `validate_literal` that takes three arguments: `value`, `allowed_set`, and `var_name`. The function does not return anything.

3. Inside the `validate_literal` function, check if the `value` is not in the `allowed_set`. If it is not, raise a `ValueError` with a message indicating that the `var_name` argument must be one of the values in the `allowed_set`.

4. Define a function named `validate_literals` that takes one argument: `arguments`. The function does not return anything.

5. Inside the `validate_literals` function, iterate over each `arg` in the `arguments` list.

6. For each `arg`, extract the `var_name`, `allowed_set`, and `value` from the `arg` dictionary.

7. Check if the `value` is an instance of a list or tuple. If it is, iterate over each `val` in the `value` list.

8. For each `val`, call the `validate_literal` function with the arguments `value=val`, `allowed_set=allowed_set`, and `var_name=var_name`.

9. If the `value` is not a list or tuple, call the `validate_literal` function with the arguments `value=value`, `allowed_set=allowed_set`, and `var_name=var_name`.

10. Define a function named `validate_paths` that takes two arguments: `startpath` and `destination`. The function returns a tuple of `Path` objects.

11. Inside the `validate_paths` function, check if the `startpath` is not an instance of a string or `PathLike` object. If it is not, raise a `TypeError` with a message indicating that a `Path-like` object or string is expected for the `startpath` argument.

12. Check if the `destination` is not an instance of a string or `PathLike` object. If it is not, raise a `TypeError` with a message indicating that a `Path-like` object or string is expected for the `destination` argument.

13. Convert the `startpath` to a `Path` object for easier manipulation.

14. Create a new `Path` object by concatenating the `startpath` and `destination`.

15. Check if the `startpath` does not have read permission. If it does not, raise a `PermissionError` with a message indicating that read permission is required for the `startpath`.

16. Check if the `destination` does not have write permission. If it does not, raise a `PermissionError` with a message indicating that write permission is required for the `destination` path.

17. Return the `startpath` and `destination` as a tuple.

18. Define a function named `validate_temperature` that takes one argument: `temperature`. The function returns an `int` or `float`.

19. Inside the `validate_temperature` function, try to convert the `temperature` to an `int`. If it succeeds, assign the converted value to the variable `int_temperature` and return it.

20. If the conversion to `int` raises a `ValueError`, continue to the next step.

21. Try to convert the `temperature` to a `float`. If it succeeds, assign the converted value to the variable `float_temperature`.

22. If the conversion to `float` raises a `ValueError`, raise a `ValueError` with a message indicating that the `temperature` argument must be convertible to an `int` or `float`.

23. Check if the `float_temperature` is less than 0 or greater than 1. If it is, raise a `ValueError` with a message indicating that the `temperature` argument must be between 0 and 1.

24. Return the `float_temperature`.

# dir_diary\classifier.py
2023-09-13 10:25:47
1. Import the following objects:
   - ProjectFile from the file_handler module
   - query_llm from the chatbot module
   - FileClassification and FileClassificationList from the datastructures module
   - Path from the pathlib module
   - PromptTemplate from the langchain module
   - ChatOpenAI from the langchain.chat_models module
   - PydanticOutputParser from the langchain.output_parsers module
   - json

2. Define a function named "initialize_project_map" that takes a Path argument named "project_map_path" and returns a FileClassificationList object.
   - Initialize a FileClassificationList object named "project_map" with an empty list of files.
   - Check if the project map file exists.
     - If it exists and is empty, print a warning message and return the empty project map.
     - If it exists and is not empty, open the file and load its contents as a list of dictionaries named "project_map_json".
       - Validate the "project_map_json" using the FileClassificationList model and assign the validated object to "project_map".
   - Return the project map.

3. Define a function named "update_project_map" that takes two arguments: "project_map" of type FileClassificationList and "project_files" of type list[ProjectFile]. It returns a FileClassificationList object.
   - Create a list named "existing_paths" that contains the paths of files in the "project_map" for easier lookup.
   - Iterate over each "new_file" in "project_files".
     - If the path of "new_file" is not in "existing_paths", append a new FileClassification object with the path of "new_file" and a role of None to the "project_map" files list.
   - Update the "project_map" files list to only include files whose paths are in the paths of "project_files".
   - Return the updated project map.

4. Create a PydanticOutputParser object named "parser" with the pydantic_object set to FileClassificationList.

5. Create a PromptTemplate object named "file_classification_prompt" with the following properties:
   - template: A string containing a template for classifying files based on their roles in a project.
   - input_variables: A list containing a single string variable named "input_str".
   - partial_variables: A dictionary containing a single key-value pair where the key is "format_instructions" and the value is the format instructions obtained from the "parser" object.
   - output_parser: The "parser" object.

6. Define a function named "classify_files" that takes four arguments: "project_map_file" of type Path, "project_files" of type list[ProjectFile], "llm" of type ChatOpenAI, and "long_context_llm" of type ChatOpenAI. It returns a list of ProjectFile objects.
   - Get the project map by calling the "initialize_project_map" function with "project_map_path" set to "project_map_file".
   - Update the project map by calling the "update_project_map" function with "project_map" set to the obtained project map and "project_files" set to "project_files".
   - Check if any files in the project map have a role of None.
     - If none of the files have a role of None, call the "assign_roles" function with "project_map" set to the obtained project map and "project_files" set to "project_files".
     - Return the updated project files.
   - Convert the project map to a JSON string and assign it to "input_str".
   - Query the LLM by calling the "query_llm" function with the following arguments:
     - prompt: The "file_classification_prompt" object.
     - input_str: The obtained "input_str".
     - llm: The "llm" object.
     - long_context_llm: The "long_context_llm" object.
     - parser: The "parser" object.
   - If the project map is not empty, write it to the project map file.
     - Create the parent directory of the project map file if it doesn't exist.
     - Open the project map file in write mode and write the JSON-formatted project map to it.
   - Call the "assign_roles" function with "project_map" set to the obtained project map and "project_files" set to "project_files".
   - Return the updated project files.

7. Define a function named "assign_roles" that takes two arguments: "project_map" of type FileClassificationList and "project_files" of type list[ProjectFile]. It returns a list of ProjectFile objects.
   - Create a dictionary named "mapping" that maps the paths of files in "project_map" to their roles.
   - Iterate over each "file" in "project_files".
     - Assign the role of "file" to the corresponding role in "mapping" based on the file's path.
   - Return the updated project files.

# dir_diary\cli.py
2023-09-13 15:02:10
The code imports the following objects:
- `summarize_project_folder` function from the `summarize` module
- `click` module
- `pprint` module

The code defines a command-line interface (CLI) using the `click.command()` decorator. The CLI has the following options:
- `--startpath`: Specifies the path to the project folder. Default value is the current directory.
- `--destination`: Specifies the destination folder for the generated files. Default value is "docs".
- `--include`: Specifies the types of files to include in the summary. Default value is ["source", "utility scripts"].
- `--summary_types`: Specifies the types of summaries to generate. Default value is ["pseudocode"].
- `--api_key`: Specifies the API key for OpenAI. Default value is None.
- `--model_name`: Specifies the name of the OpenAI model to use. Default value is "gpt-3.5-turbo".
- `--long_context_fallback`: Specifies the fallback model for long context. Default value is "gpt-3.5-turbo-16k".
- `--temperature`: Specifies the temperature for the OpenAI model. Default value is 0.

The `cli` function is defined with the following arguments:
- `startpath`: Path to the project folder.
- `destination`: Destination folder for the generated files.
- `summary_types`: Types of summaries to generate.
- `include`: Types of files to include.
- `api_key`: API key for OpenAI.
- `model_name`: Name of the OpenAI model.
- `long_context_fallback`: Fallback model for long context.
- `temperature`: Temperature for the OpenAI model.

The `cli` function calls the `summarize_project_folder` function with the specified arguments.

# dir_diary\datastructures.py
2023-09-13 16:59:12
- Import the necessary modules: `typing`, `pathlib`, `datetime`, `pydantic`, and `json`.
- Define a set of allowed summary types, roles, models, and fallbacks.
- Define a class called `ProjectFile` that inherits from `BaseModel`.
  - It has attributes `path`, `modified`, and `role`.
  - The `role` attribute is an optional literal value from a predefined set of roles.
- Define a class called `FileClassification` that inherits from `BaseModel`.
  - It has attributes `path` and `role`.
  - Both attributes are optional literal values from a predefined set of roles.
- Define a class called `FileClassificationList` that inherits from `BaseModel`.
  - It has an attribute `files` which is a list of `FileClassification` objects.
  - It has a method called `to_json` that converts the `FileClassificationList` object to a JSON-formatted string.
- Define a class called `ModuleSummary` that inherits from `BaseModel`.
  - It has attributes `path`, `modified`, and `content`.

# dir_diary\file_handler.py
2023-09-13 16:48:55
Pseudocode Summary:

Imported Objects:
- ModuleSummary (from .datastructures)
- ProjectFile (from .datastructures)
- Path (from pathlib)
- datetime (from datetime)

Function: read_summary_file
- Input: summary_file (Path)
- Output: list[ModuleSummary]
- Create an empty list called "summaries"
- If the summary file does not exist:
  - Create the file
  - Return the empty list "summaries"
- Read the contents of the file
- For each section introduced by a single-hashed header:
  - Split the section into lines
  - If there are not enough lines, skip to the next section
  - Extract the path from the first line
  - Convert the modified timestamp to a datetime object
  - Extract the content from the remaining lines
  - Create a ModuleSummary object with the extracted information
  - Append the ModuleSummary object to the "summaries" list
- Return the "summaries" list

Function: write_summary_file
- Input: summaries (list[ModuleSummary]), summary_file (Path)
- Output: None
- Create an empty string called "contents"
- For each ModuleSummary object in the "summaries" list:
  - Add a single-hashed header with the path to the "contents" string
  - Add the modified timestamp to the "contents" string
  - Add the content to the "contents" string
- If the "summaries" list is not empty:
  - Create the parent directory of the summary file if it doesn't exist
  - Write the "contents" string to the summary file

Function: identify_new_and_modified_files
- Input: summaries (list[ModuleSummary]), project_files (list[ProjectFile])
- Output: tuple[list[ProjectFile], list[ProjectFile]]
- Create a mapping of 'path' to 'modified' from the "summaries" list
- Create empty lists called "new_files" and "modified_files"
- For each ProjectFile object in the "project_files" list:
  - If the path is not in the summaries map, add the file to "new_files"
  - If the file's 'modified' time is later than the corresponding entry in the summaries map, add the file to "modified_files"
- Return the tuple of "new_files" and "modified_files"

Function: remove_deleted_files_from_summaries
- Input: summaries (list[ModuleSummary]), files (list[ProjectFile])
- Output: list[ModuleSummary]
- Convert the "files" list into a set of paths called "file_paths"
- Filter the "summaries" list to include only files present in "file_paths"
- Return the filtered "summaries" list

# dir_diary\mapper.py
2023-09-12 11:21:54
1. Import the necessary modules and objects:
   - `os` module
   - `pathspec` module
   - `Path` object from the `pathlib` module
   - `datetime` object from the `datetime` module
   - `ProjectFile` class from the `file_handler` module

2. Define a function named `map_project_folder` that takes an optional argument `startpath` and returns a list of `ProjectFile` objects.
   - Convert `startpath` to a `Path` object.
   - Initialize an empty list `paths_and_modifications` to store the paths and modifications.

3. Walk the directory tree starting from `startpath`.
   - For each directory, add the files to the list.
   - For each file, create a `Path` object for the file path.
   - Get the relative file path with respect to `startpath`.
   - Get the modified time of the file and format it as a string.
   - Create a `ProjectFile` object with the relative file path and modified time, and append it to `paths_and_modifications`.

4. Return the `paths_and_modifications` list.

5. Define a function named `remove_gitignored_files` that takes two optional arguments `startpath` and `project_files`, and returns a list of `ProjectFile` objects.
   - Convert `startpath` to a `Path` object.
   - Get a list of all `ProjectFile` objects in `project_files` whose file name is ".gitignore" and assign it to `gitignore_files`.
   - Create a copy of `project_files` and assign it to `filtered_files`.
   - Remove files with a parent directory containing ".git" from `filtered_files`.
   - Iterate over the `gitignore_files`.
     - Get the directory containing the `.gitignore` file and assign it to `gitignore_dir`.
     - Read the contents of the `.gitignore` file and assign it to `lines`.
     - Create a `pathspec.GitIgnoreSpec` object from the `lines` and assign it to `spec`.
     - Get the subset of `filtered_files` that are in the same directory tree as the `.gitignore` file and assign it to `same_dir_files`.
     - Get the subset of `same_dir_files` that match the `spec` and assign it to `to_remove`.
     - Remove the matching files from `filtered_files`.
   - Return the `filtered_files` list.

6. If the script is being run directly:
   - Import the `map_project_folder` function from the `dir_diary.mapper` module.
   - Call the `map_project_folder` function with `startpath` set to "." and assign the result to `paths_list`.
   - Iterate over `paths_list` and print the path and modified time of each entry.

# dir_diary\summarize.py
2023-09-13 20:42:52
The code is a function called `summarize_project_folder` that takes several arguments to summarize a project folder. Here is the pseudocode summary:

1. Import necessary objects and functions from various modules.
2. Define the function `summarize_project_folder` with the following arguments:
   - `startpath`: The path to the project folder (default is current directory).
   - `destination`: The path to the destination folder where the summaries will be saved (default is "docs").
   - `summary_types`: A list of summary types to generate (default is ["pseudocode"]).
   - `include`: A list of project roles to include in the summaries (default is ["source", "utility scripts"]).
   - `api_key`: The API key for the OpenAI chatbot (default is None).
   - `model_name`: The name of the chatbot model to use (default is "gpt-3.5-turbo").
   - `long_context_fallback`: The name of the chatbot model to use as a fallback for long context (default is "gpt-3.5-turbo-16k").
   - `temperature`: The temperature parameter for the chatbot (default is 0).
3. Validate the literal argument values for `summary_types`, `include`, `model_name`, and `long_context_fallback`.
4. Validate the path arguments `startpath` and `destination`.
5. Validate the temperature argument.
6. Initialize the OpenAI chatbot with the specified parameters and a cost tracker.
7. If `long_context_fallback` is not None, initialize a second chatbot.
8. Map the project folder and get a list of `ProjectFile` objects.
9. Remove all project files listed in `.gitignore`.
10. Classify the project files by project role using the chatbot.
11. Keep only project files with roles that are in the `include` list.
12. For each summary type in both `summary_types` and `["pseudocode", "usage"]`:
    - Create or read the summary file for the type.
    - Get a list of existing summaries.
    - Remove any files that have been deleted from the summaries.
    - Identify new and modified files since the last summary.
    - If there are no files to summarize and the updated summaries are identical to the existing summaries, exit.
    - For each file to summarize, query the chatbot for an updated summary.
    - Drop any existing summaries for the file and add the generated summary to the updated summaries.
    - Write the updated summaries to the summary file.
13. Print the total cost of the workflow run.
14. Return None.

# dir_diary\summarizer.py
2023-09-13 17:46:38
1. Import the following objects:
   - Literal from the typing module
   - ModuleSummary and ProjectFile from the file_handler module
   - query_llm from the chatbot module
   - PromptTemplate from the langchain module
   - ChatOpenAI from the langchain.chat_models module

2. Define a PromptTemplate object named "pseudocode_prompt" with a template string for generating a pseudocode summary.

3. Define a PromptTemplate object named "usage_prompt" with a template string for generating a usage summary.

4. Define a function named "summarize_file" that takes the following arguments:
   - file_to_summarize: a ProjectFile object representing the file to be summarized
   - summary_type: a Literal type indicating whether to generate a pseudocode or usage summary
   - llm: a ChatOpenAI object representing the chatbot to query
   - long_context_llm: a string representing the long context for the chatbot

5. Read the content of the file_to_summarize and store it in the input_str variable.

6. Determine the prompt to use based on the summary_type argument.

7. Query the chatbot using the query_llm function, passing the prompt, input_str, llm, long_context_llm, and None as arguments. Store the generated summary in the generated_summary variable.

8. Create a ModuleSummary object named "module_summary" with the path, modified, and generated_summary as arguments.

9. Return the module_summary object.

# dir_diary\__init__.py
2023-09-13 16:53:55
- Import the `summarize_project_folder` function from the `summarize` module.
- Import the `read_summary_file` function and the `ModuleSummary` class from the `file_handler` module.
- Define the `__all__` list containing the names of the functions and classes that will be accessible when importing this package. The list includes "summarize_project_folder", "read_summary_file", and "ModuleSummary".

