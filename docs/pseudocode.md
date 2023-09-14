# dir_diary\chatbot.py
2023-09-12 20:59:27
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

# dir_diary\classifier.py
2023-09-12 20:59:27
The code includes the following functions and classes:

1. Function: `initialize_project_map(project_map_path: Path) -> FileClassificationList`
   - Initializes a project map from a JSON file.
   - Returns a `FileClassificationList` object.

2. Function: `update_project_map(project_map: FileClassificationList, project_files: list[ProjectFile]) -> FileClassificationList`
   - Updates the project map with new files and removes deleted files.
   - Returns the updated `FileClassificationList` object.

3. Class: `PydanticOutputParser`
   - Parses the output of the LLM (Language Model) and returns a `FileClassificationList` object.

4. Class: `PromptTemplate`
   - Represents a template for querying the chatbot to determine the role of files in a project.
   - Contains a template string, input variables, partial variables, and an output parser.

5. Function: `classify_files(project_map_file: Path, project_files: list[ProjectFile], llm: ChatOpenAI, long_context_llm: ChatOpenAI) -> list[ProjectFile]`
   - Queries a chatbot to determine the role of files in a project.
   - Returns a list of `ProjectFile` objects with assigned roles.

6. Function: `assign_roles(project_map: FileClassificationList, project_files: list[ProjectFile]) -> list[ProjectFile]`
   - Assigns roles to project files based on the corresponding roles in the project map.
   - Returns the updated list of `ProjectFile` objects.

The execution sequence is as follows:

1. Import necessary modules and classes.
2. Initialize a `PydanticOutputParser` object.
3. Define a `PromptTemplate` object for querying the chatbot.
4. Define the `initialize_project_map` function.
   - Initialize an empty `FileClassificationList` object.
   - If the project map file exists, load the project map from the JSON file.
   - Return the project map.
5. Define the `update_project_map` function.
   - Create a list of existing paths in the project map for easier lookup.
   - Add new files to the project map and remove deleted files.
   - Return the updated project map.
6. Define the `classify_files` function.
   - Get the project map from the JSON file or initialize an empty one.
   - Update the project map with new files and remove deleted files.
   - If all project map files have assigned roles, assign roles to project files and return them.
   - Convert the project map to an input string.
   - Query the chatbot to update the project map.
   - If the project map is not empty, write it to the project map file.
   - Assign roles to project files based on the corresponding roles in the project map.
   - Return the updated project files.
7. Define the `assign_roles` function.
   - Create a mapping of project files entries to project map roles by path.
   - Use the mapping to add roles to project files.
   - Return the updated project files.

# dir_diary\cli.py
2023-09-12 20:59:27
The code imports the `summarize_project_folder` function from the `summarize` module and the `click` module. It then defines a command-line interface using the `click.command()` decorator.

The command-line interface has several options:
- `--startpath`: Specifies the path to the project folder. Default value is "." (current directory).
- `--destination`: Specifies the destination folder for the generated files. Default value is "docs".
- `--include`: Specifies the types of files to include in the summary. Default value is ["source", "utility scripts"].
- `--summary_types`: Specifies the types of summaries to generate. Default value is ["pseudocode"].
- `--api_key`: Specifies the API key for OpenAI. Default value is None.
- `--model_name`: Specifies the name of the OpenAI model to use. Default value is "gpt-3.5-turbo".
- `--long_context_fallback`: Specifies the fallback model for long context. Default value is "gpt-3.5-turbo-16k".
- `--temperature`: Specifies the temperature for the OpenAI model. Default value is 0.

The `cli` function is the entry point of the command-line interface. It takes the above options as arguments and has a return type of None. The function's docstring describes its purpose, which is to summarize a project folder using pseudocode.

Inside the `cli` function, the `summarize_project_folder` function is called with the following arguments:
- `startpath`: The value of the `--startpath` option.
- `destination`: The value of the `--destination` option.
- `summary_types`: The value of the `--summary_types` option.
- `include`: The value of the `--include` option.
- `api_key`: The value of the `--api_key` option.
- `model_name`: The value of the `--model_name` option.
- `long_context_fallback`: The value of the `--long_context_fallback` option.
- `temperature`: The value of the `--temperature` option.

# dir_diary\datastructures.py
2023-09-12 20:59:27
- Import necessary modules: typing, pathlib, datetime, pydantic, json
- Define a set of allowed summary types, roles, and models
- Define a function named "validate_value" that takes in a value, an allowed set, and a variable name as arguments and returns None
  - If the value is not in the allowed set, raise a ValueError with a specific error message
- Define a function named "validate_arguments" that takes in a list of arguments as an argument and returns None
  - For each argument in the list
    - Get the variable name, allowed set, and value from the argument
    - If the value is a list or tuple
      - For each value in the list or tuple, call the "validate_value" function with the value, allowed set, and variable name as arguments
    - Else, call the "validate_value" function with the value, allowed set, and variable name as arguments
- Define a class named "ProjectFile" that inherits from "BaseModel"
  - Define attributes: path (of type Path), modified (of type datetime), role (optional, with allowed values specified)
- Define a class named "FileClassification" that inherits from "BaseModel"
  - Define attributes: path (of type Path), role (optional, with allowed values specified)
- Define a class named "FileClassificationList" that inherits from "BaseModel"
  - Define attribute: files (a list of FileClassification objects)
  - Define a method named "to_json" that returns a JSON-formatted string representation of the FileClassificationList object
    - Convert Path objects in the files list to strings
    - Convert the FileClassificationList object to a dictionary using the model_dump method
    - Convert the dictionary to a JSON-formatted string using the json.dumps function
- Define a class named "ModulePseudocode" that inherits from "BaseModel"
  - Define attributes: path (of type Path), modified (of type datetime), content (of type str)

# dir_diary\file_handler.py
2023-09-12 20:59:27
**Function: read_pseudocode_file(pseudocode_file: Path) -> list[ModulePseudocode]**

Given a pseudocode.md file path, this function reads the file and creates a list of ModulePseudocode objects from the file. If the file does not exist, it creates the file and returns an empty list.

1. Create an empty list called "pseudocode".
2. If the pseudocode file does not exist:
   - Create the file.
   - Return the empty list.
3. Read the contents of the file.
4. For each section introduced by a single-hashed header:
   - Split the section into lines.
   - If there are not enough lines, skip to the next section.
   - Extract the path from the first line.
   - Convert the modified timestamp to a datetime object.
   - Extract the content from the remaining lines.
   - Create a ModulePseudocode object with the extracted information.
   - Append the ModulePseudocode object to the "pseudocode" list.
5. Return the "pseudocode" list.

**Function: write_pseudocode_file(pseudocode: list[ModulePseudocode], pseudocode_file: Path) -> None**

Given a list of ModulePseudocode objects, this function creates a pseudocode.md file and writes the contents of the objects to the file.

1. Create an empty string called "contents".
2. For each ModulePseudocode object in the "pseudocode" list:
   - Add a single-hashed header with the path to the "contents" string.
   - Add the modified timestamp to the "contents" string.
   - Add the content to the "contents" string.
3. Write the "contents" string to the pseudocode file.

**Function: identify_new_and_modified_files(pseudocode: list[ModulePseudocode], project_files: list[ProjectFile]) -> tuple[list[ProjectFile], list[ProjectFile]]**

Given a list of ModulePseudocode objects and a list of ProjectFile objects, this function filters the project_files list to output a tuple of new_files missing from the pseudocode file and modified_files with 'modified' timestamps later than the 'modified' timestamps for the corresponding files in the pseudocode.

1. Create a mapping of 'path' to 'modified' from the pseudocode list.
2. Filter the project_files list:
   - If the path is not in the pseudocode map, add the file to new_files.
   - If a file's 'modified' time is later than listed in the pseudocode file, add the file to modified_files.
3. Return the filtered lists of files as a tuple.

**Function: remove_deleted_files_from_pseudocode(pseudocode: list[ModulePseudocode], files: list[ProjectFile]) -> list[ModulePseudocode]**

Given a list of ModulePseudocode objects and a list of ProjectFile objects, this function filters the pseudocode list to omit any files missing from the files list.

1. Convert the files list into a set of paths for faster lookup.
2. Filter the pseudocode list to include only files present in the files set.
3. Return the filtered pseudocode list.

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

# dir_diary\summarize.py
2023-09-12 20:59:27
**Function:** summarize_project_folder(startpath, destination, summary_types, include, api_key, model_name, long_context_fallback, temperature)

**Arguments:**
- startpath: Union[str, PathLike] (default: ".") - The path to the project folder to be summarized.
- destination: Union[str, PathLike] (default: "docs") - The destination folder where the pseudocode.md file will be created.
- summary_types: Literal["pseudocode", "usage", "tech stack"] (default: ["pseudocode"]) - The type of summary to generate.
- include: list[Literal["source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"]] (default: ["source", "utility scripts"]) - The roles of project files to include in the summary.
- api_key: str (default: None) - The API key for the OpenAI chatbot.
- model_name: Literal["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613"] (default: "gpt-3.5-turbo") - The name of the chatbot model to use.
- long_context_fallback: Literal["gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"] (default: "gpt-3.5-turbo-16k") - The name of the chatbot model to use as a fallback for long contexts.
- temperature: float (default: 0) - The temperature parameter for the chatbot model.

**Execution:**
1. Validate the values of 'summary_types', 'include', 'model_name', and 'long_context_fallback'.
2. Create the paths for the pseudocode.md file and the project_map.json file.
3. Map the project folder and store the list of ProjectFile objects.
4. Remove all project_files listed in .gitignore.
5. Initialize the OpenAI chatbot and the cost tracker.
6. If long_context_fallback is not None, initialize a second chatbot.
7. Classify the project files by project role.
8. Keep only project files with roles that are in the include list.
9. Read or create the pseudocode file and get the ModulePseudocode list.
10. Filter the pseudocode summary to remove any files that have been deleted.
11. Identify new and modified files since the last summary.
12. If there are no files to summarize and the updated pseudocode is identical to the existing pseudocode, exit.
13. For each file to summarize, query the chatbot for an updated pseudocode summary.
14. Drop any existing pseudocode for the file and add the output to the updated pseudocode.
15. Write the updated pseudocode to the pseudocode file.
16. Print the total cost of the workflow run.
17. Return.

# dir_diary\summarizer.py
2023-09-12 20:59:27
1. Import the necessary modules and classes:
   - Import `ModulePseudocode` and `ProjectFile` from the `file_handler` module.
   - Import `query_llm` from the `chatbot` module.
   - Import `PromptTemplate` from the `langchain` module.
   - Import `ChatOpenAI` from the `langchain.chat_models` module.

2. Define a prompt template for generating a pseudocode summary of a code module.

3. Define a function named `summarize_file` that takes three arguments:
   - `file_to_summarize` of type `ProjectFile`: The file to be summarized.
   - `llm` of type `ChatOpenAI`: The chatbot used for generating the summary.
   - `long_context_llm` of type `str`: The long context for the chatbot.

4. Read the content of the file specified by `file_to_summarize` and store it in the variable `input_str`.

5. Query the chatbot using the `query_llm` function, passing the `summarization_prompt` template, `input_str`, `llm`, `long_context_llm`, and `parser` as arguments. Store the generated pseudocode in the variable `generated_pseudocode`.

6. Create a `ModulePseudocode` object named `module_pseudocode` using the `file_to_summarize.path`, `file_to_summarize.modified`, and `generated_pseudocode` as arguments.

7. Return the `module_pseudocode` object as the output of the function.

# dir_diary\__init__.py
2023-09-12 20:59:27
- Import the `summarize_project_folder` function from the `summarize` module.
- Import the `read_pseudocode_file` function and the `ModulePseudocode` class from the `file_handler` module.
- Define the `__all__` list containing the names of the functions and classes that will be accessible when importing this module. The list includes `summarize_project_folder`, `read_pseudocode_file`, and `ModulePseudocode`.

