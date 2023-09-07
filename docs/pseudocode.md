# pseudocode_summarizer\mapper.py
2023-09-06 12:28:34
Pseudocode Summary:

1. Import the necessary modules: os, pathspec, Path, datetime, and ProjectFile from file_handler.
2. Define a function called "map_project_folder" that takes a parameter "startpath" with a default value of "." and returns a list of ProjectFile objects.
3. Convert the "startpath" parameter to a Path object.
4. Initialize an empty list called "paths_and_modifications" to store the paths and modifications.
5. Use the os.walk() function to traverse the directory tree starting from the "startpath".
6. For each root, _, files in the directory tree:
   - Iterate over the files.
   - Create a Path object for the file.
   - Get the relative file path by removing the "startpath" from the file path.
   - Get the modified time of the file and format it as a string.
   - Create a ProjectFile object with the relative file path and modified time, and append it to the "paths_and_modifications" list.
7. Return the "paths_and_modifications" list.
8. Define a function called "remove_gitignored_files" that takes two parameters: "startpath" with a default value of "." and "project_files" with a default value of a ProjectFile object representing the ".gitignore" file.
9. Convert the "startpath" parameter to a Path object.
10. Get a list of all ".gitignore" files in the "project_files" list.
11. Create a copy of the "project_files" list called "filtered_files".
12. Iterate over the ".gitignore" files:
    - Get the directory containing the ".gitignore" file.
    - Read the lines of the ".gitignore" file.
    - Create a pathspec object from the lines of the ".gitignore" file.
    - Get the subset of "filtered_files" that are in the directory tree of the ".gitignore" file.
    - Get the subset of "same_dir_files" that match the pathspec.
    - Remove the matching files from the "filtered_files" list.
13. Return the "filtered_files" list.
14. If the script is being run directly:
    - Import the "map_project_folder" function from the "pseudocode_summarizer" module.
    - Call the "map_project_folder" function with the "startpath" parameter set to "." and assign the result to "paths_list".
    - Iterate over the "paths_list" and print the "path" and "modified" attributes of each entry.

# pseudocode_summarizer\file_handler.py
2023-09-07 13:22:18
**Function: read_pseudocode_file**

This function takes a `pseudocode_file` path as an argument and returns a list of `ModulePseudocode` objects. If the `pseudocode_file` does not exist, it creates the file and returns an empty list. 

1. Create an empty list called `pseudocode`.
2. Check if the `pseudocode_file` does not exist.
   - If true, create the file and return the empty `pseudocode` list.
3. Read the contents of the file.
4. Split the contents into sections using single-hashed headers.
   - Skip the first (empty) section.
5. For each section:
   - Split the section into lines.
   - Check if there are enough lines.
     - If not, continue to the next section.
   - Extract the path from the first line.
   - Convert the modified timestamp to a datetime object.
   - Extract the content from the remaining lines.
   - Create a `ModulePseudocode` object with the extracted values.
   - Validate the object using Pydantic.
   - Append the object to the `pseudocode` list.
6. Return the `pseudocode` list.

**Function: write_pseudocode_file**

This function takes a list of `ModulePseudocode` objects (`pseudocode`) and a `pseudocode_file` path as arguments. It creates a pseudocode.md file based on the `pseudocode` list.

1. Create an empty string called `contents`.
2. For each `module` in the `pseudocode` list:
   - Add a single-hashed header with the path to the `contents` string.
   - Add the modified timestamp to the `contents` string.
   - Add the content to the `contents` string.
   - Add a blank line to the `contents` string.
3. Write the `contents` string to the `pseudocode_file`.
   - If the `pseudocode` list is not empty, create the parent directory of the `pseudocode_file` if it doesn't exist.
4. Return None.

**Function: identify_new_and_modified_files**

This function takes a list of `ModulePseudocode` objects (`pseudocode`) and a list of `ProjectFile` objects (`project_files`) as arguments. It filters the `project_files` list to output two lists: `new_files` (files missing from `pseudocode`) and `modified_files` (files with modified timestamps later than those in `pseudocode`).

1. Create a mapping of `path` to `modified` from the `pseudocode` list.
2. Create empty lists called `new_files` and `modified_files`.
3. For each `file` in the `project_files` list:
   - Check if the `path` is not in the `pseudocode` map.
     - If true, append the `file` to the `new_files` list.
   - Check if the `modified` timestamp of the `file` is later than the one listed in `pseudocode`.
     - If true, append the `file` to the `modified_files` list.
4. Return a tuple containing the `new_files` and `modified_files` lists.

**Function: remove_deleted_files_from_pseudocode**

This function takes a list of `ModulePseudocode` objects (`pseudocode`) and a list of `ProjectFile` objects (`files`) as arguments. It filters the `pseudocode` list to remove any files missing from the `files` list.

1. Convert the `files` list into a set of paths called `file_paths` for faster lookup.
2. Filter the `pseudocode` list to include only files present in `files`.
3. Return the filtered `pseudocode` list.

# pseudocode_summarizer\summarizer.py
2023-09-07 14:23:12
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

# pseudocode_summarizer\chatbot.py
2023-09-07 15:31:00
1. Import necessary libraries and modules: os, dotenv, typing, langchain.chat_models, langchain, openai.error, langchain.output_parsers, langchain.callbacks, pydantic.BaseModel.
2. Define a function named "initialize_model" with the following arguments:
   - api_key (string, optional): API key for OpenAI.
   - temperature (float, optional): Temperature parameter for the chatbot model.
   - model_name (string, optional): Name of the chatbot model.
   - callbacks (list, optional): List of callback functions.
3. If no API key is provided, load it from the .env file or environment.
4. Create a chatbot instance using the langchain module with the provided arguments.
5. Return the chatbot instance.
6. Define a function named "query_llm" with the following arguments:
   - prompt (PromptTemplate): Template for the chatbot prompt.
   - input_str (string): Input string for the chatbot.
   - llm (ChatOpenAI): Chatbot instance.
   - long_context_llm (ChatOpenAI): Chatbot instance with long context.
   - parser (PydanticOutputParser, optional): Parser for the chatbot output.
7. Create a chatbot chain using the langchain module with the provided arguments.
8. Generate the output from the input using the chatbot chain.
9. If an InvalidRequestError is raised, check if long_context_llm is None.
   - If long_context_llm is None, raise the error.
   - If long_context_llm is not None, print a warning message and use long_context_llm.
10. Parse the output using the provided parser.
11. If no parser is provided, return the raw output.
12. If a parser is provided, parse the output and return the parsed output.

# pseudocode_summarizer\summarize.py
2023-09-07 18:28:47
Function: summarize_project_folder(startpath, pseudocode_file, project_map_file, include, api_key, model_name, long_context_fallback, temperature)

1. Set pseudocode_file as the path to the pseudocode file in the startpath directory.
2. Set project_map_file as the path to the project map file in the startpath directory.
3. Map the project folder using the startpath and store the list of ProjectFile objects in project_files.
4. Remove all project_files listed in .gitignore using the startpath and project_files.
5. Initialize the OpenAI chatbot with the given api_key, temperature, model_name, and cost_tracker callback.
6. If long_context_fallback is not None, initialize a second chatbot with the given api_key, temperature, model_name, and cost_tracker callback.
7. Classify the project_files by project role using the project_map_file, project_files, llm, and long_context_llm.
8. Keep only project files with roles that are in the include list.
9. Read or create the pseudocode file and get the list of ModulePseudocode objects in pseudocode.
10. Filter the pseudocode summary to remove any files that have been deleted using the pseudocode and project_files.
11. Identify new and modified files since the last summary using the pseudocode and project_files, and store them in new_files and modified_files.
12. Combine new_files and modified_files into files_to_summarize.
13. If there are no files_to_summarize and updated_pseudocode is identical to pseudocode, exit the function.
14. Sort the updated_pseudocode and pseudocode lists.
15. For each file in files_to_summarize, summarize the file using the file, llm, and long_context_llm, and store the generated pseudocode in generated_pseudocode.
16. Remove any existing pseudocode for the file from updated_pseudocode.
17. Add the generated pseudocode to updated_pseudocode.
18. Write the updated pseudocode to the pseudocode file.
19. Print the total cost of the workflow run.
20. Return.

# pseudocode_summarizer\cli.py
2023-09-07 18:35:38
The code imports the `summarize_project_folder` function from a module called `summarize`. It also imports the `click` module.

The code defines a command-line interface (CLI) using the `click.command()` decorator. The CLI has several options that can be passed as command-line arguments. The options include `startpath`, `pseudocode_file`, `project_map_file`, `include`, `api_key`, `model_name`, `long_context_fallback`, and `temperature`. Each option has a default value and a help message.

The code defines a function called `cli` that takes the arguments `startpath`, `pseudocode_file`, `project_map_file`, `include`, `api_key`, `model_name`, `long_context_fallback`, and `temperature`. The function is decorated with the `click.command()` decorator.

The function `cli` has a docstring that describes its purpose, which is to summarize a project folder using pseudocode.

Inside the `cli` function, the `summarize_project_folder` function is called with the arguments `startpath`, `pseudocode_file`, `project_map_file`, `include`, `api_key`, `model_name`, `long_context_fallback`, and `temperature`.

# pseudocode_summarizer\classifier.py
2023-09-07 19:09:42
The code includes the following functions and classes:

1. Class: FileClassification
   - Data structure for LLM classification of project file roles
   - Attributes:
     - path: Path (file path relative to the project root)
     - role: Optional[Literal[...]] (role the file plays in the project)

2. Class: FileClassificationList
   - Data structure for a list of FileClassifications
   - Attributes:
     - files: list[FileClassification] (List of file classifications)
   - Method: to_json()
     - Converts a FileClassificationList to a JSON-formatted string

3. Function: initialize_project_map(project_map_path: Path) -> FileClassificationList
   - Initializes a project map from a JSON file
   - Arguments:
     - project_map_path: Path (path to the project map JSON file)
   - Returns:
     - FileClassificationList (initialized project map)

4. Function: update_project_map(project_map: FileClassificationList, project_files: list[ProjectFile]) -> FileClassificationList
   - Updates the project map with new files and removes deleted files
   - Arguments:
     - project_map: FileClassificationList (current project map)
     - project_files: list[ProjectFile] (list of project files)
   - Returns:
     - FileClassificationList (updated project map)

5. Class: PydanticOutputParser
   - Parser for the LLM output
   - Arguments:
     - pydantic_object: FileClassificationList

6. Class: PromptTemplate
   - Prompt template for determining the roles that files play in the project
   - Attributes:
     - template: str (template string)
     - input_variables: list[str] (input variable names)
     - partial_variables: dict (partial variable names and values)
     - output_parser: PydanticOutputParser

7. Function: classify_files(project_map_file: Path, project_files: list[ProjectFile], llm: ChatOpenAI, long_context_llm: ChatOpenAI) -> list[ProjectFile]
   - Queries a chatbot to determine the role that files play in the project
   - Arguments:
     - project_map_file: Path (path to the project map JSON file)
     - project_files: list[ProjectFile] (list of project files)
     - llm: ChatOpenAI (chatbot for short context)
     - long_context_llm: ChatOpenAI (chatbot for long context)
   - Returns:
     - list[ProjectFile] (updated list of project files)

8. Function: assign_roles(project_map: FileClassificationList, project_files: list[ProjectFile]) -> list[ProjectFile]
   - Assigns roles to project files based on corresponding roles in project_map
   - Arguments:
     - project_map: FileClassificationList (project map with file classifications)
     - project_files: list[ProjectFile] (list of project files)
   - Returns:
     - list[ProjectFile] (updated list of project files)

# pseudocode_summarizer\__init__.py
2023-09-07 19:24:13
- Import the `summarize_project_folder` function from the `summarize` module.
- Import the `read_pseudocode_file` function and the `ModulePseudocode` class from the `file_handler` module.
- Define the `__all__` list containing the names of the functions and classes that will be accessible when importing this module. The list includes "summarize_project_folder", "read_pseudocode_file", and "ModulePseudocode".

