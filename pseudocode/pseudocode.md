# pseudocode_summarizer\chatbot.py
2023-09-05 15:22:53
The pseudocode summary of the given code is as follows:

1. Import the necessary modules: os, ChatOpenAI from langchain.chat_models, and load_dotenv from dotenv.
2. Define a function named "initialize_model" that takes three parameters: api_key (a string), temperature (a float), and model_name (a string). The function returns an instance of the ChatOpenAI class.
3. Inside the function:
   a. Check if the api_key parameter is None.
   b. If api_key is None, load the API key from the .env file or environment using the load_dotenv function and os.getenv method. Print a message indicating that the API key is being used from the .env file.
   c. Create an instance of the ChatOpenAI class named "llm" with the provided api_key, model_name, max_tokens (set to 2000), and temperature.
   d. Return the "llm" instance.

# pseudocode_summarizer\classifier.py
2023-09-06 14:47:01
The code begins by importing necessary modules and dependencies. It imports the `ProjectFile` class from the `file_handler` module, the `Path` class from the `pathlib` module, various classes and functions from the `langchain` module, the `ChatOpenAI` class from the `chat_models` module, the `PydanticOutputParser` class from the `output_parsers` module, the `json` module, and some classes and functions from the `typing` and `pydantic` modules.

Next, it defines two data structures using the `BaseModel` class from the `pydantic` module. The first data structure is called `FileClassification` and represents the classification of a project file. It has two fields: `path`, which represents the file path relative to the project root, and `role`, which represents the role the file plays in the project. The `role` field is an optional field with a default value of `None`.

The second data structure is called `FileClassificationList` and represents a list of `FileClassification` objects. It has one field: `files`, which is a list of `FileClassification` objects.

After that, there is a method defined within the `FileClassificationList` class called `to_json()`. This method converts a `FileClassificationList` object to a JSON-formatted string. It first converts the `FileClassificationList` object to a dictionary using the `dict()` method, excluding any fields that have not been set. Then, it iterates over the `files` list and converts any `Path` objects to strings. Finally, it uses the `json.dumps()` function to convert the dictionary to a JSON-formatted string and returns it.

The code then defines a function called `initialize_project_map()` that takes a `project_map_path` argument of type `Path` and returns a `FileClassificationList` object. It initializes a default empty `FileClassificationList` object called `project_map`. If the `project_map_path` file exists and is not empty, it reads the JSON data from the file, parses it into a list of dictionaries, and converts it to a `FileClassificationList` object using the `parse_obj()` method. Finally, it returns the `project_map` object.

Next, there is a function called `update_project_map()` that takes a `project_map` argument of type `FileClassificationList` and a `project_files` argument of type `list[ProjectFile]`, and returns a `FileClassificationList` object. It creates a list called `existing_paths` that contains the paths of the files in the `project_map` object. Then, it iterates over the `project_files` list and adds any files that are not already in the `project_map` object, with a `None` role. It also removes any files from the `project_map` object that are not in the `project_files` list. Finally, it returns the updated `project_map` object.

The code then creates an instance of the `PydanticOutputParser` class called `parser`, passing a `pydantic_object` argument of type `FileClassificationList`.

Next, there is a `PromptTemplate` object called `file_classification_prompt` that represents a template for a chatbot prompt. It contains a template string that describes the task and provides instructions for classifying files. It also specifies input variables and a partial variable for the format instructions, and an output parser.

After that, there is a function called `classify_files()` that takes a `project_map_file` argument of type `Path`, a `project_files` argument of type `list[ProjectFile]`, and an `llm` argument of type `ChatOpenAI`, and returns a `list[ProjectFile]`. It first calls the `initialize_project_map()` function to get the `project_map` object. Then, it calls the `update_project_map()` function to update the `project_map` object with new files and remove deleted files. If all files in the `project_map` object have a role assigned, it returns the `project_files` list as is. Otherwise, it creates an instance of the `LLMChain` class called `llm_chain`, passing the `llm` argument, the `file_classification_prompt` object, and a `verbose` argument set to `True`. It converts the `project_map` object to a JSON-formatted string and assigns it to the `_input` variable. It queries the LLM chain with the `_input` string and assigns the output to the `output` variable. It parses the output text using the `parser` object and assigns the result to the `project_map` object. If the `project_map` object is not empty, it writes it to the `project_map_file` as a JSON-formatted string. It creates a mapping of file paths to roles from the `project_map` object. It then iterates over the `project_files` list and assigns the corresponding role from the mapping to each file. Finally, it returns the updated `project_files` list.

The pseudocode summary of the code is as follows:

```
Import necessary modules and dependencies

Define FileClassification data structure
    - path: Path
    - role: Optional[Literal[...]]

Define FileClassificationList data structure
    - files: list[FileClassification]

Define to_json() method in FileClassificationList
    - Convert FileClassificationList to dictionary
    - Convert Path objects to strings
    - Convert dictionary to JSON-formatted string
    - Return JSON-formatted string

Define initialize_project_map() function
    - Initialize empty FileClassificationList object
    - If project map file exists and is not empty
        - Read JSON data from file
        - Parse JSON data into list of dictionaries
        - Convert list of dictionaries to FileClassificationList object
    - Return FileClassificationList object

Define update_project_map() function
    - Create list of existing paths in project_map
    - For each new file in project_files
        - If file path not in existing paths, add it to project_map with None role
    - Remove any paths in project_map that are not in project_files
    - Return updated project_map

Create instance of PydanticOutputParser class called parser

Create PromptTemplate object called file_classification_prompt

Define classify_files() function
    - Get project_map from project_map_file or initialize empty one
    - Update project_map with new files and remove deleted files
    - If all files in project_map have roles assigned, return project_files
    - Create LLMChain instance called llm_chain
    - Convert project_map to JSON-formatted string
    - Query LLMChain with input string
    - Parse output text using parser
    - If project_map is not empty, write it to project_map_file
    - Create mapping of file paths to roles from project_map
    - Assign roles to project_files based on mapping
    - Return updated project_files
```

# pseudocode_summarizer\file_handler.py
2023-09-06 14:52:07
Pseudocode Summary:

1. Import necessary modules and classes: `Path` from `pathlib`, `datetime` from `datetime`, `BaseModel`, `Field`, `ValidationError` from `pydantic`, and `Optional`, `Literal` from `typing`.
2. Define a Pydantic class `ModulePseudocode` with attributes `path`, `modified`, and `content`.
3. Define a Pydantic class `ProjectFile` with attributes `path`, `modified`, and `role`.
4. Define a function `read_pseudocode_file` that takes a `pseudocode_file` path and returns a list of `ModulePseudocode` objects.
5. Inside `read_pseudocode_file`, create an empty list `pseudocode`.
6. Check if the `pseudocode_file` does not exist. If true, create the file and return the empty `pseudocode` list.
7. Read the contents of the file and store it in the `contents` variable.
8. Split the `contents` into sections using the single-hashed header as the separator.
9. Iterate over each section, skipping the first (empty) section.
10. Split each section into lines.
11. Check if the number of lines is less than 3. If true, continue to the next section.
12. Extract the path, modified timestamp, and content from the lines.
13. Create a `ModulePseudocode` object with the extracted values and validate it using Pydantic.
14. Append the `module` object to the `pseudocode` list.
15. Return the `pseudocode` list.
16. Define a function `write_pseudocode_file` that takes a `pseudocode` list and a `pseudocode_file` path and writes the `pseudocode` to the file.
17. Inside `write_pseudocode_file`, create an empty string `contents`.
18. Iterate over each `module` in the `pseudocode` list.
19. Add a single-hashed header with the path to the `contents` string.
20. Add the modified timestamp and content to the `contents` string.
21. Write the `contents` string to the `pseudocode_file`.
22. Define a function `identify_new_and_modified_files` that takes a `pseudocode` list and a `project_files` list and returns a tuple of `new_files` and `modified_files`.
23. Inside `identify_new_and_modified_files`, create a mapping of `path` to `modified` from the `pseudocode` list.
24. Iterate over each `file` in the `project_files` list.
25. If the `file` path is not in the `pseudocode_map`, add it to the `new_files` list.
26. If the `file`'s `modified` time is later than the corresponding `modified` time in the `pseudocode_map`, add it to the `modified_files` list.
27. Return the `new_files` and `modified_files` lists.
28. Define a function `remove_deleted_files_from_pseudocode` that takes a `pseudocode` list and a `files` list and returns a filtered `pseudocode` list.
29. Inside `remove_deleted_files_from_pseudocode`, convert the `files` list into a set of paths for faster lookup.
30. Filter the `pseudocode` list to include only files present in the `files` set.
31. Return the filtered `pseudocode` list.

# pseudocode_summarizer\legacy.py
2023-09-05 11:39:30
The code begins by importing necessary modules and dependencies. It imports the `Literal` type from the `typing` module, the `Path` class from the `pathlib` module, various classes and functions from the `langchain` package, the `BaseModel` and `Field` classes from the `pydantic` module, and the `initialize_model` function from a `chatbot` module.

Next, it defines two data structures using the `BaseModel` class from `pydantic`. The first is the `FileClassification` class, which has two fields: `path` (a string representing the file path relative to the project root) and `classification` (a literal type with possible values of "include" or "ignore" representing whether to include or ignore the file). The second is the `FileClassificationList` class, which has a single field `files` (a list of `FileClassification` objects).

Then, it creates an instance of the `PydanticOutputParser` class, passing in the `FileClassificationList` class as the `pydantic_object` parameter. This parser will be used to parse the output of the chatbot into a `FileClassificationList` object.

After that, it defines a `PromptTemplate` object named `file_classification_prompt`. This object represents a template for a prompt that will be used to query the chatbot. It has a `template` attribute that contains a string with placeholders for variables, an `input_variables` attribute that specifies the names of the variables that will be passed as input to the prompt, and a `partial_variables` attribute that contains a dictionary of partial variables used in the template.

Next, it defines a function named `classify_new_files` that takes in a list of new file paths, an API key, a model name, and a temperature as parameters. Inside the function, it initializes an OpenAI chatbot by calling the `initialize_model` function with the provided API key, temperature, and model name. 

Then, it generates a prompt for the chatbot by calling the `format_prompt` method of the `file_classification_prompt` object, passing in the new file paths as the `file_paths` variable. This generates a string prompt that includes the file paths and format instructions.

The generated prompt is then passed as input to the chatbot by calling the `llm` object with the prompt converted to a list of messages using the `to_messages` method of the `_input` object. The output of the chatbot is stored in the `output` variable.

The output of the chatbot is then parsed into a `FileClassificationList` object by calling the `parse` method of the `parser` object, passing in the content of the output as the `text` parameter. The parsed output is stored in the `parsed_output` variable.

Next, the list of `FileClassifications` in the parsed output is filtered into two separate lists: `include_files` and `ignore_files`. This is done by iterating over each `FileClassification` object in the `files` attribute of the `parsed_output` object and checking its `classification` field. If the `classification` is "include", the file path is added to the `include_files` list. If the `classification` is "ignore", the file path is added to the `ignore_files` list.

Finally, the function returns the `include_files` and `ignore_files` lists as a tuple.

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

# pseudocode_summarizer\summarizer.py
2023-09-06 14:54:04
The code imports the necessary modules and types from various libraries. It defines a string variable `summarize_template` which contains a prompt for generating a pseudocode summary. 

The `summarize_file` function takes two parameters: `file_to_summarize` of type `ProjectFile` and `llm` of type `ChatOpenAI`. It reads the content of the file specified by `file_to_summarize` and assigns it to the `input` variable. 

It creates an instance of the `LLMChain` class called `llm_chain`, passing in the `llm` object, the `summarize_template` prompt, and setting the `verbose` flag to `True`. 

The `llm_chain` object is then used to generate an output by passing in the `input` variable. The output is stored in the `output` variable. 

A `ModulePseudocode` object called `generated_pseudocode` is created using the `ModulePseudocode` class, with the `path`, `modified`, and `content` attributes set to the corresponding values from `file_to_summarize` and `output['text']`. 

Finally, the `generated_pseudocode` object is returned.

# pseudocode_summarizer\__init__.py
2023-09-06 10:51:03
The code is an __init__.py file that imports various functions and classes from different modules and makes them available for use. The imported objects include:
- map_project_folder and remove_gitignored_files from the mapper module
- read_pseudocode_file, write_pseudocode_file, identify_new_and_modified_files, remove_deleted_files_from_pseudocode, ModulePseudocode, and ProjectFile from the file_handler module
- initialize_model from the chatbot module
- classify_files, FileClassification, and FileClassificationList from the classifier module
- summarize_file from the summarizer module
- summarize_project_folder from the summarize module

All the imported objects are added to the __all__ list, which specifies the objects that will be imported when using the "from module import *" syntax.

# pseudocode_summarizer\chatbot.py
2023-09-07 14:57:38
1. Import necessary libraries and modules.
2. Define a function called "initialize_model" with the following arguments:
   - api_key (string, optional)
   - temperature (float, optional)
   - model_name (string, optional)
   - callbacks (list, optional)
   The function returns a ChatOpenAI object.
3. Inside the "initialize_model" function:
   - Check if an API key is provided. If not, load it from the .env file or environment.
   - Create a ChatOpenAI object called "llm" with the provided arguments.
   - Return the "llm" object.
4. Define a function called "query_llm" with the following arguments:
   - prompt (PromptTemplate)
   - input_str (string)
   - llm (ChatOpenAI)
   - long_context_llm (ChatOpenAI)
   - parser (PydanticOutputParser, optional)
   The function returns a BaseModel object.
5. Inside the "query_llm" function:
   - Create an LLMChain object called "llm_chain" with the provided arguments.
   - Try to generate the output from the input using the "llm_chain" object.
   - If an InvalidRequestError is raised, check if "long_context_llm" is None.
     - If it is None, raise the error.
     - If it is not None, print a warning message, update the "llm_chain" object with "long_context_llm", and generate the output again.
   - If no parser is provided, return the raw output.
   - If a parser is provided, parse the output using the "parser" object.
   - Return the parsed output.

# pseudocode_summarizer\classifier.py
2023-09-07 14:11:49
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

# pseudocode_summarizer\summarize.py
2023-09-07 14:54:21
Function: summarize_project_folder(startpath, pseudocode_file, project_map_file, include, api_key, model_name, long_context_fallback, temperature)

1. Set pseudocode_file as the path to the pseudocode file in the startpath directory.
2. Set project_map_file as the path to the project map file in the startpath directory.
3. Map the project folder using the startpath and store the list of ProjectFile objects in project_files.
4. Remove all project_files listed in .gitignore using the startpath and project_files.
5. Initialize the OpenAI chatbot with the given api_key, temperature, model_name, and cost_tracker callback.
6. If long_context_fallback is not None, initialize a second chatbot with the same parameters and the long_context_llm callback.
7. Classify the project_files by project role using the project_map_file, project_files, llm, and long_context_llm.
8. Keep only the project_files with roles that are in the include list.
9. Read or create the pseudocode file and get the list of ModulePseudocode objects in pseudocode.
10. Filter the pseudocode summary to remove any files that have been deleted using the pseudocode and project_files.
11. Identify the new and modified files since the last summary using the pseudocode and project_files, and store them in new_files and modified_files.
12. Combine the new_files and modified_files into the files_to_summarize list.
13. If there are no files_to_summarize and the updated_pseudocode is identical to the pseudocode, exit the function.
14. Sort the updated_pseudocode and pseudocode lists by path and modified date.
15. For each file in the files_to_summarize list, summarize the file using the file, llm, and long_context_llm, and store the generated pseudocode in generated_pseudocode.
16. Add the generated_pseudocode to the updated_pseudocode list.
17. Write the updated_pseudocode to the pseudocode file.
18. Print the total cost of the workflow run using the cost_tracker.
19. Return.

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

# pseudocode_summarizer\__init__.py
2023-09-07 13:38:39
The code is importing various functions and classes from different modules. It is also defining the "__all__" list to specify the names that should be imported when using the "from . import *" syntax. 

The imported functions and classes include:
- map_project_folder: a function that maps the project folder
- remove_gitignored_files: a function that removes gitignored files
- read_pseudocode_file: a function that reads a pseudocode file
- write_pseudocode_file: a function that writes a pseudocode file
- identify_new_and_modified_files: a function that identifies new and modified files
- classify_new_files: a function that classifies new files
- remove_deleted_files_from_pseudocode: a function that removes deleted files from pseudocode
- ModulePseudocode: a class representing module pseudocode
- ProjectFile: a class representing a project file
- summarize_file: a function that summarizes a file
- initialize_model: a function that initializes a model
- classify_files: a function that classifies files
- FileClassification: a class representing file classification
- FileClassificationList: a class representing a list of file classifications
- summarize_project_folder: a function that summarizes a project folder
- query_llm: a function that queries a language model

