# dir_diary/datastructures.py
2023-09-12 00:00:28
- Import necessary modules: typing, pathlib, datetime, pydantic, json
- Define a set of allowed summary types, roles, and models
- Define a function named "validate_value" that takes in three arguments: value, allowed_set, and var_name. It validates if the value is in the allowed set and raises a ValueError if it is not.
- Define a function named "validate_arguments" that takes in one argument: arguments. It iterates through each argument and calls the "validate_value" function to validate the value.
- Define a class named "ProjectFile" that inherits from "BaseModel". It has three attributes: path (of type Path), modified (of type datetime), and role (of type Optional[Literal]). The role attribute has a default value of None and a description.
- Define a class named "FileClassification" that inherits from "BaseModel". It has two attributes: path (of type Path) and role (of type Optional[Literal]). The role attribute has a default value of None and a description.
- Define a class named "FileClassificationList" that inherits from "BaseModel". It has one attribute: files (a list of FileClassification objects) and a description. It also has a method named "to_json" that converts the FileClassificationList object to a JSON-formatted string.
- Define a class named "ModulePseudocode" that inherits from "BaseModel". It has three attributes: path (of type Path), modified (of type datetime), and content (of type str).

# dir_diary/__init__.py
2023-09-12 00:00:28
- Import the `summarize_project_folder` function from the `summarize` module.
- Import the `read_pseudocode_file` function and the `ModulePseudocode` class from the `file_handler` module.
- Define the `__all__` list containing the names of the functions and classes that will be accessible when importing this module. The list includes "summarize_project_folder", "read_pseudocode_file", and "ModulePseudocode".

# dir_diary/mapper.py
2023-09-12 00:00:28
Pseudocode Summary:

1. Import the necessary modules: os, pathspec, Path, datetime, and ProjectFile from file_handler.
2. Define a function called "map_project_folder" that takes an optional argument "startpath" and returns a list of ProjectFile objects.
3. Convert the "startpath" argument to a Path object.
4. Initialize an empty list called "paths_and_modifications" to store the paths and modifications.
5. Walk the directory tree starting from the "startpath".
6. For each file in the directory, create a ProjectFile object with the relative file path and modified time, and append it to the "paths_and_modifications" list.
7. Return the "paths_and_modifications" list.
8. Define a function called "remove_gitignored_files" that takes two optional arguments: "startpath" and "project_files" (default value is a ProjectFile object representing the .gitignore file).
9. Convert the "startpath" argument to a Path object.
10. Get a list of all .gitignore files in the "project_files" list.
11. Create a copy of the "project_files" list called "filtered_files".
12. Iterate over each .gitignore file.
13. Get the directory containing the .gitignore file.
14. Read the contents of the .gitignore file.
15. Create a pathspec object from the lines of the .gitignore file.
16. Get the subset of "filtered_files" that are in the same directory tree as the .gitignore file.
17. Get the subset of "same_dir_files" that match the pathspec.
18. Remove the matching files from the "filtered_files" list.
19. Return the "filtered_files" list.
20. If the script is being run directly (not imported), execute the following code:
    a. Import the "map_project_folder" function from the "dir_diary.mapper" module.
    b. Call the "map_project_folder" function with the "startpath" argument set to "." and assign the result to "paths_list".
    c. Iterate over each entry in "paths_list" and print the "path" and "modified" attributes.

# dir_diary/summarize.py
2023-09-12 00:00:28
**Function:** summarize_project_folder(startpath, destination, summary_types, include, api_key, model_name, long_context_fallback, temperature)

1. **Arguments:**
   - startpath: Union[str, PathLike] = "."
   - destination: Union[str, PathLike] = "docs"
   - summary_types: Literal["pseudocode", "usage", "tech stack"] = ["pseudocode"]
   - include: list[Literal["source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"]] = ["source", "utility scripts"]
   - api_key: str = None
   - model_name: Literal["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613"] = "gpt-3.5-turbo"
   - long_context_fallback: Literal["gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"] = "gpt-3.5-turbo-16k"
   - temperature: float = 0

2. **Validate 'include', 'model_name', and 'long_context_fallback' values:**
   - validate_arguments(arguments=[{'var_name': 'summary_types', 'allowed_set': ALLOWED_SUMMARY_TYPES, 'value': summary_types}, {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': include}, {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': model_name}, {'var_name': 'long_context_fallback', 'allowed_set': ALLOWED_MODELS, 'value': long_context_fallback}])

3. **Get relative file paths by prepending startpath:**
   - pseudocode_file: Path = Path(startpath) / Path(destination) / "pseudocode.md"
   - project_map_file: Path = Path(startpath) / Path(destination) / "project_map.json"

4. **Map the project folder, outputting a list of ProjectFile objects:**
   - project_files: list[ProjectFile] = map_project_folder(startpath=startpath)

5. **Remove all project_files listed in .gitignore:**
   - project_files: list[ProjectFile] = remove_gitignored_files(startpath=startpath, project_files=project_files)

6. **Initialize OpenAI chatbot:**
   - cost_tracker: OpenAICallbackHandler = OpenAICallbackHandler()
   - llm: ChatOpenAI = initialize_model(api_key=api_key, temperature=temperature, model_name=model_name, callbacks=[cost_tracker])

7. **If long_context_fallback is not None, initialize a second chatbot:**
   - if long_context_fallback is not None:
     - long_context_llm: ChatOpenAI = initialize_model(api_key=api_key, temperature=temperature, model_name=long_context_fallback, callbacks=[cost_tracker])
   - else:
     - long_context_llm = None

8. **Classify files by project role:**
   - project_files: list[ProjectFile] = classify_files(project_map_file=project_map_file, project_files=project_files, llm=llm, long_context_llm=long_context_llm)

9. **Keep only project files with roles that are in the include list:**
   - project_files: list[ProjectFile] = [file for file in project_files if file.role in include]

10. **Read or create the pseudocode file and get ModulePseudocode list:**
    - pseudocode: list[ModulePseudocode] = read_pseudocode_file(pseudocode_file=pseudocode_file)

11. **Filter pseudocode summary to remove any files that have been deleted:**
    - updated_pseudocode: list[ModulePseudocode] = remove_deleted_files_from_pseudocode(pseudocode=pseudocode, files=project_files)

12. **Output ProjectFile lists of new and modified files since last summary:**
    - new_files, modified_files = identify_new_and_modified_files(pseudocode=pseudocode, project_files=project_files)
    - files_to_summarize: list[ProjectFile] = new_files + modified_files

13. **If there are no files_to_summarize and updated_pseudocode is identical to pseudocode, exit:**
    - sorted_updated_pseudocode = sorted(updated_pseudocode, key=lambda x: (x.path, x.modified))
    - sorted_pseudocode = sorted(pseudocode, key=lambda x: (x.path, x.modified))
    - if not files_to_summarize and sorted_updated_pseudocode == sorted_pseudocode:
      - return

14. **For each file_to_summarize, query the chatbot for an updated_pseudocode summary:**
    - for file in files_to_summarize:
      - generated_pseudocode: ModulePseudocode = summarize_file(file_to_summarize=file, llm=llm, long_context_llm=long_context_llm)
      - updated_pseudocode = [pseudocode for pseudocode in updated_pseudocode if pseudocode.path != file.path]
      - updated_pseudocode.append(generated_pseudocode)

15. **Write the updated pseudocode to the pseudocode file:**
    - write_pseudocode_file(pseudocode=updated_pseudocode, pseudocode_file=pseudocode_file)

16. **Print the total cost of the workflow run:**
    - print("Total cost of workflow run: " + str(object=cost_tracker.total_cost))

17. **Return None**

# dir_diary/chatbot.py
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

# dir_diary/summarizer.py
2023-09-12 00:00:28
1. Import the necessary modules and classes:
   - `ModulePseudocode` from `file_handler`
   - `ProjectFile` from `file_handler`
   - `query_llm` from `chatbot`
   - `PromptTemplate` from `langchain`
   - `ChatOpenAI` from `langchain.chat_models`

2. Define a prompt template for generating a pseudocode summary of a code module.

3. Define a function named `summarize_file` that takes three arguments:
   - `file_to_summarize` of type `ProjectFile`
   - `llm` of type `ChatOpenAI`
   - `long_context_llm` of type `str`

4. Read the content of the file specified by `file_to_summarize` and store it in the variable `input_str`.

5. Query the chatbot (`llm`) to generate a pseudocode summary using the `query_llm` function. Pass the `summarization_prompt` template as the prompt, `input_str` as the input string, `llm` as the chatbot model, `long_context_llm` as the long context, and `None` as the parser.

6. Create a `ModulePseudocode` object named `module_pseudocode` using the output of the chatbot query. Set the `path` attribute to the path of the `file_to_summarize`, the `modified` attribute to the modified timestamp of the `file_to_summarize`, and the `content` attribute to the generated pseudocode.

7. Return the `module_pseudocode` object as the result of the function.

# dir_diary/file_handler.py
2023-09-12 00:00:28
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
3. Return the tuple of new_files and modified_files.

**Function: remove_deleted_files_from_pseudocode(pseudocode: list[ModulePseudocode], files: list[ProjectFile]) -> list[ModulePseudocode]**

Given a list of ModulePseudocode objects and a list of ProjectFile objects, this function filters the pseudocode list to omit any files missing from the files list.

1. Convert the files list into a set of paths for faster lookup.
2. Filter the pseudocode list to include only files present in the files set.
3. Return the filtered pseudocode list.

# dir_diary/classifier.py
2023-09-12 00:00:28
The code includes the following functions and classes:

1. `initialize_project_map(project_map_path: Path) -> FileClassificationList`: 
   - This function initializes a project map from a JSON file.
   - It takes a `project_map_path` argument, which is the path to the JSON file.
   - It returns a `FileClassificationList` object, which represents the project map.

2. `update_project_map(project_map: FileClassificationList, project_files: list[ProjectFile]) -> FileClassificationList`:
   - This function updates the project map with new files and removes deleted files.
   - It takes two arguments: `project_map`, which is the current project map, and `project_files`, which is a list of new project files.
   - It returns the updated `FileClassificationList` object.

3. `classify_files(project_map_file: Path, project_files: list[ProjectFile], llm: ChatOpenAI, long_context_llm: ChatOpenAI) -> list[ProjectFile]`:
   - This function queries a chatbot to determine the role that files play in the project.
   - It takes four arguments: `project_map_file`, which is the path to the project map JSON file, `project_files`, which is a list of project files, `llm`, which is a chatbot model for short context, and `long_context_llm`, which is a chatbot model for long context.
   - It returns a list of `ProjectFile` objects, which represents the updated project files.

4. `assign_roles(project_map: FileClassificationList, project_files: list[ProjectFile]) -> list[ProjectFile]`:
   - This function assigns roles to project files based on corresponding roles in the project map.
   - It takes two arguments: `project_map`, which is the project map, and `project_files`, which is a list of project files.
   - It returns the updated list of `ProjectFile` objects.

The code also includes the following objects and variables:

- `parser`: An instance of the `PydanticOutputParser` class.
- `file_classification_prompt`: An instance of the `PromptTemplate` class.
- `existing_paths`: A list of existing paths in the project map for easier lookup.
- `project_map_json`: A list of dictionaries representing the project map in JSON format.
- `input_str`: A string representation of the project map in JSON format.

The execution sequence is as follows:

1. Import necessary modules and classes.
2. Initialize the `parser` object with a `PydanticOutputParser` instance.
3. Initialize the `file_classification_prompt` object with a `PromptTemplate` instance.
4. Define the `initialize_project_map` function.
5. Define the `update_project_map` function.
6. Define the `classify_files` function.
7. Define the `assign_roles` function.
8. The code block outside the functions initializes the `parser` object with a `PydanticOutputParser` instance.
9. The code block outside the functions initializes the `file_classification_prompt` object with a `PromptTemplate` instance.
10. The code block outside the functions defines the `existing_paths` variable.
11. The code block outside the functions defines the `project_map_json` variable.
12. The code block outside the functions defines the `input_str` variable.
13. The code block outside the functions assigns the `parser` object to the `output_parser` attribute of the `file_classification_prompt` object.
14. The code block outside the functions defines the `project_map` variable and initializes it with an empty `FileClassificationList`.
15. The code block outside the functions checks if the project map file exists and is empty.
16. The code block outside the functions opens the project map file and loads its contents as a JSON object.
17. The code block outside the functions assigns the loaded JSON object to the `project_map` variable.
18. The code block outside the functions returns the `project_map` variable.
19. The code block outside the functions creates a list of existing paths in the project map for easier lookup.
20. The code block outside the functions iterates over the new project files and adds them to the project map if they are not already present.
21. The code block outside the functions removes any paths in the project map that are not in the new project files.
22. The code block outside the functions returns the updated project map.
23. The code block outside the functions checks if any project map files have a `None` role.
24. The code block outside the functions assigns roles to project files based on corresponding roles in the project map.
25. The code block outside the functions returns the updated project files.
26. The code block outside the functions converts the project map to a JSON string.
27. The code block outside the functions queries the LLM with the file classification prompt and the project map JSON string.
28. The code block outside the functions updates the project map with the LLM output.
29. The code block outside the functions checks if the project map is not empty.
30. The code block outside the functions writes the project map to the project map file.
31. The code block outside the functions assigns roles to project files based on corresponding roles in the project map.
32. The code block outside the functions returns the updated project files.

# dir_diary/cli.py
2023-09-12 00:00:28
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

