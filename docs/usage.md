# dir_diary\classifier.py
2023-09-16 16:25:57
To use the code, you will need to import several modules and objects:

```python
from .file_handler import ProjectFile
from .openai_chatbot import classify_with_openai
from .datastructures import FileClassification, FileClassificationList
from pathlib import Path
import json
```

To initialize a project map from a JSON file, use the `initialize_project_map` function. Pass in the path to the project map JSON file as a `Path` object. The function will return a `FileClassificationList` object, which represents the project map.

```python
project_map_path = Path("path/to/project_map.json")
project_map = initialize_project_map(project_map_path)
```

To update the project map with new files and remove deleted files, use the `update_project_map` function. Pass in the current project map as a `FileClassificationList` object and a list of `ProjectFile` objects representing the new files. The function will return the updated project map.

```python
new_files = [ProjectFile(path="path/to/new_file.png"), ProjectFile(path="path/to/another_file.txt")]
updated_project_map = update_project_map(project_map, new_files)
```

To query a chatbot to determine the role that files play in the project, use the `classify_files` function. Pass in the path to the project map JSON file and a list of `ProjectFile` objects representing the project files. The function will return a list of `ProjectFile` objects with assigned roles.

```python
project_map_file = Path("path/to/project_map.json")
project_files = [ProjectFile(path="path/to/file.png"), ProjectFile(path="path/to/another_file.txt")]
updated_project_files = classify_files(project_map_file, project_files)
```

There is also a helper function `assign_roles` that is used within `classify_files` to assign roles to project files based on corresponding roles in the project map. The function takes in the project map (`FileClassificationList`) and a list of project files (`list[ProjectFile]`) and returns the updated list of project files.

```python
project_map = FileClassificationList(files=[FileClassification(path="path/to/file.png", role="image"), FileClassification(path="path/to/another_file.txt", role="text")])
project_files = [ProjectFile(path="path/to/file.png"), ProjectFile(path="path/to/another_file.txt")]
updated_project_files = assign_roles(project_map, project_files)
```

Please note that some data types and classes used in the code, such as `ProjectFile`, `FileClassification`, and `FileClassificationList`, are imported from other modules (`file_handler`, `openai_chatbot`, and `datastructures`). The specific usage of these classes and functions cannot be inferred from the code provided, so you will need to refer to the corresponding modules for more information.

# dir_diary\cli.py
2023-09-15 14:31:43
To use the provided code, follow these steps:

1. Import the `summarize_project_folder` function from the `summarize` module within the package.
- Example: `from .summarize import summarize_project_folder`

2. Import the `click` module for command-line interface functionality.
- Example: `import click`

3. Create a command-line interface by decorating a function with `@click.command()`.
- Example:
```python
@click.command()
def cli(startpath: str, destination: str, summary_types: list[str], include: list[str], api_key: str, model_name: str, long_context_fallback: str, temperature: float) -> None:
    """
    Summarize a project folder using pseudocode.
    """
```

4. Use the `@click.option()` decorator to define command-line options with their respective data types and default values.
- Available options:
  - `--startpath`: Path to the project folder. Default value is `"."`.
  - `--destination`: Destination folder for the generated files. Default value is `"docs"`.
  - `--include`: Types of files to include. Default value is `["source", "utility scripts"]`. Valid choices include:
    - `"source"`
    - `"configuration"`
    - `"build or deployment"`
    - `"documentation"`
    - `"testing"`
    - `"database"`
    - `"utility scripts"`
    - `"assets or data"`
    - `"specialized"`
  - `--summary_types`: Types of summaries to generate. Default value is `["pseudocode"]`. Valid choices include:
    - `"pseudocode"`
    - `"usage"`
    - `"tech stack"`
  - `--api_key`: API key for OpenAI. Default value is `None`.
  - `--model_name`: Name of the OpenAI model. Default value is `"gpt-3.5-turbo"`. Valid choices include:
    - `"gpt-3.5-turbo"`
    - `"gpt-3.5-turbo-0301"`
    - `"gpt-3.5-turbo-0613"`
    - `"gpt-3.5-turbo-16k"`
    - `"gpt-3.5-turbo-16k-0613"`
    - `"gpt-4"`
    - `"gpt-4-0314"`
    - `"gpt-4-0613"`
  - `--long_context_fallback`: Fallback model for long context. Default value is `"gpt-3.5-turbo-16k"`. Valid choices include:
   - `"gpt-4"`
   - `"gpt-4-0314"`
   - `"gpt-4-0613"`
   - `"gpt-3.5-turbo-16k"`
   - `"gpt-3.5-turbo-16k-0613"`
  - `--temperature`: Temperature for the OpenAI model. Default value is 0.
  
5. Define the function body for the command-line interface function. In this case, the function calls the `summarize_project_folder` function with the provided arguments.
- Example:
```python
def cli(startpath: str, destination: str, summary_types: list[str], include: list[str], api_key: str, model_name: str, long_context_fallback: str, temperature: float) -> None:
    """
    Summarize a project folder using pseudocode.
    """
    summarize_project_folder(
        startpath=startpath, 
        destination=destination,
        summary_types=summary_types,
        include=include,
        api_key=api_key, 
        model_name=model_name, 
        long_context_fallback=long_context_fallback, 
        temperature=temperature
    )
```

6. To invoke the command-line interface and run the code, execute the Python script with the appropriate command-line arguments.
- Example: `python my_script.py --startpath /path/to/project --destination /path/to/destination`

Note: The specific functionality and expected data types of the `summarize_project_folder` function and any imported functions or classes from other modules are not provided in the code and may need to be inferred from the actual implementation in those modules.

# dir_diary\client.py
2023-09-15 18:06:26
To use the provided code, follow these instructions:

1. Import the necessary modules:
   - `from .validators import validate_temperature, validate_api_key` (uncertain origin)
   - `from dotenv import load_dotenv`
   - `from os import getenv`
   - `from typing import Optional, Union`

2. Create an instance of the `LLMClient` class:
   - `client = LLMClient(api_key, model_name, long_context_fallback, temperature, total_cost)`

3. Use the `api_key`, `model_name`, `long_context_fallback`, `temperature`, and `total_cost` variables as arguments when creating the instance. These arguments have the following data types:
   - `api_key: Optional[str]` (optional) - Represents the API key as a string. It can be obtained from the .env file or environment. If not provided, it will be loaded from the .env file or environment using `load_dotenv()` and `getenv(key="OPENAI_API_KEY")`.
   - `model_name: str` - Represents the name of the model as a string.
   - `long_context_fallback: Optional[str]` (optional) - Represents the name of the long context fallback as a string. If not provided, it defaults to "gpt-3.5-turbo-16k".
   - `temperature: float` - Represents the temperature value as a float. It is used to control the randomness of the generated text.
   - `total_cost: Optional[Union[float, int]]` (optional) - Represents the total cost as either a float or an integer. If not provided, it defaults to 0.

4. Any subsequent calls to create an instance of `LLMClient` will return the same instance, as it is implemented as a Singleton pattern.
   - `client = LLMClient()` (returns the existing instance)

Note: The code includes private variables (_instance and _initialized) and dunder methods (`__new__` and `__init__`) that are responsible for the Singleton behavior and initialization of the class.

---

Imported functions and their usages:

1. `validate_temperature(temperature: float) -> float`:
   - Description: Validates the temperature value and returns it if it is within the valid range.
   - Usage: `valid_temperature = validate_temperature(temperature)`

2. `validate_api_key(api_key: str) -> str`:
   - Description: Validates the API key and returns it if it is valid.
   - Usage: `valid_api_key = validate_api_key(api_key)`

Imported modules:

1. `load_dotenv()` (from `dotenv` module):
   - Description: Loads environment variables from the .env file into the current session.
   - Usage: `load_dotenv()`

2. `getenv(key="OPENAI_API_KEY")` (from `os` module):
   - Description: Retrieves the value of the specified environment variable.
   - Usage: `api_key = getenv(key="OPENAI_API_KEY")`

Note: The usages for the imported modules' functions are inferred based on their traditional usage.

# dir_diary\datastructures.py
2023-09-16 13:16:39
To use the provided code, follow these instructions:

1. Import the necessary modules:
   - `from typing import Optional, Literal` (import data types for function arguments and class methods)
   - `from pathlib import Path` (import the `Path` class for working with file paths)
   - `from datetime import datetime` (import the `datetime` class for working with timestamps)
   - `from pydantic import BaseModel, Field` (import the `BaseModel` class and `Field` decorator for defining data structures)

2. Define the allowed summary types, roles, models, and fallbacks:
   - `ALLOWED_SUMMARY_TYPES`: A set containing the allowed summary types. Valid values are "pseudocode", "usage", and "tech stack".
   - `ALLOWED_ROLES`: A set containing the allowed roles. Valid values are "source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", and "specialized".
   - `ALLOWED_MODELS`: A set containing the allowed models. Valid values are specific versions of the GPT model.
   - `ALLOWED_FALLBACKS`: A set containing the allowed fallback models.

3. Define the data structure for project file metadata:
   - Create a class `ProjectFile` that inherits from `BaseModel`.
   - Add the following attributes to the class:
     - `path`: A `Path` object representing the file path.
     - `modified`: A `datetime` object representing the last modified timestamp of the file.
     - `role`: An optional attribute that specifies the role of the file in the project. Valid values are the allowed roles defined in `ALLOWED_ROLES`.

4. Define the data structure for file classification:
   - Create a class `FileClassification` that inherits from `BaseModel`.
   - Add the following attributes to the class:
     - `path`: A `Path` object representing the file path relative to the project root.
     - `role`: An optional attribute that specifies the role of the file. Valid values are the allowed roles defined in `ALLOWED_ROLES`.

5. Define the data structure for a list of file classifications:
   - Create a class `FileClassificationList` that inherits from `BaseModel`.
   - Add the following attribute to the class:
     - `files`: A list of `FileClassification` objects representing file classifications.
   - Implement the `to_json` method that converts the `FileClassificationList` object to a JSON-formatted string. This method uses the `json.dumps` function to serialize the object.

6. Define the data structure for module summary:
   - Create a class `ModuleSummary` that inherits from `BaseModel`.
   - Add the following attributes to the class:
     - `path`: A `Path` object representing the file path of the module.
     - `modified`: A `datetime` object representing the last modified timestamp of the module.
     - `content`: A string representing the generated module summary.

Note: Ensure that you have the necessary dependencies installed, such as Pydantic.

Usage:

```python
from typing import Optional, Literal
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field
import json

**Define allowed summary types, roles, and models as sets**
ALLOWED_SUMMARY_TYPES = {"pseudocode", "usage", "tech stack"}
ALLOWED_ROLES = {"source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"}
ALLOWED_MODELS = {"gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613"}
ALLOWED_FALLBACKS = {'gpt-4', 'gpt-4-0314', 'gpt-4-0613', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613'}

**Data structure for project file metadata**
class ProjectFile(BaseModel):
    path: Path
    modified: datetime
    role: Optional[Literal["source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"]] = Field(
            default=None, description="role the file plays in the project"
        )

**Data structure for file classification**
class FileClassification(BaseModel):
    path: Path = Field(description="file path relative to the project root")
    role: Optional[Literal["source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"]] = Field(
            default=None, description="role the file plays in the project"
        )

**Data structure for a list of file classifications**
class FileClassificationList(BaseModel):
    files: list[FileClassification] = Field(
            description="List of file classifications"
        )

    # Method to convert a FileClassificationList to a JSON-formatted string
    def to_json(self) -> str:
        data_dict = self.model_dump(exclude_unset=True)

        # Convert Path objects to str
        for file in data_dict.get("files", []):
            file["path"] = str(object=file["path"])

        return json.dumps(obj=data_dict)

**Data structure to hold the generated module summary**
class ModuleSummary(BaseModel):
    path: Path
    modified: datetime
    content: str
```

Use the above code as a template to define your own data structures, and modify the attributes and methods as per your requirements.

# dir_diary\file_handler.py
2023-09-14 15:48:05
To use the code in `file_handler.py`, you need to follow these instructions:

1. Import the required classes and functions from other modules:
   - Import the `ModuleSummary` and `ProjectFile` classes from the `datastructures` module.
   - Import the `Path` class from the `pathlib` module.
   - Import the `datetime` class from the `datetime` module.
   - Import the `warn` function from the `warnings` module.

Example:
```python
from .datastructures import ModuleSummary, ProjectFile
from pathlib import Path
from datetime import datetime
from warnings import warn
```

2. Create instances or invoke methods of defined objects:
   - To create a list of `ModuleSummary` objects from a summary file, use the `read_summary_file` function. Pass a `Path` object representing the path to the summary file as an argument. The function will return a list of `ModuleSummary` objects parsed from the file or an empty list if the file does not exist.

   Example:
   ```python
   summary_file = Path("path/to/summary_file.txt")
   summaries = read_summary_file(summary_file)
   ```

   - To create a summary markdown file from a list of `ModuleSummary` objects, use the `write_summary_file` function. Pass the list of `ModuleSummary` objects and a `Path` object representing the path to the summary file as arguments. The function will create a summary markdown file with the path, modified timestamp, and content of each `ModuleSummary` object.

   Example:
   ```python
   summary_file = Path("path/to/summary_file.txt")
   write_summary_file(summaries, summary_file)
   ```

   - To filter a list of `ProjectFile` objects to identify new and modified files, use the `identify_new_and_modified_files` function. Pass a list of `ModuleSummary` objects and a list of `ProjectFile` objects as arguments. The function will return a tuple containing the `new_files` that are missing from the `summary_file` and the `modified_files` with modified timestamps later than the timestamps in the summaries.

   Example:
   ```python
   new_files, modified_files = identify_new_and_modified_files(summaries, project_files)
   ```

   - To filter a list of `ModuleSummary` objects to remove files missing from a list of `ProjectFile` objects, use the `remove_deleted_files_from_summaries` function. Pass a list of `ModuleSummary` objects and a list of `ProjectFile` objects as arguments. The function will return a filtered list of `ModuleSummary` objects that only includes files present in the `files` list.

   Example:
   ```python
   filtered_summaries = remove_deleted_files_from_summaries(summaries, project_files)
   ```

3. Data types:
   - The `read_summary_file` function expects a `Path` object as the `summary_file` argument and returns a list of `ModuleSummary` objects.
   - The `write_summary_file` function expects a list of `ModuleSummary` objects and a `Path` object as the `summaries` and `summary_file` arguments, respectively. It does not return anything (`None`).
   - The `identify_new_and_modified_files` function expects a list of `ModuleSummary` objects and a list of `ProjectFile` objects as the `summaries` and `project_files` arguments. It returns a tuple containing two lists of `ProjectFile` objects: `new_files` and `modified_files`.
   - The `remove_deleted_files_from_summaries` function expects a list of `ModuleSummary` objects and a list of `ProjectFile` objects as the `summaries` and `files` arguments. It returns a list of `ModuleSummary` objects.

Note: The specific data types and required imports for classes and functions imported from outside this module are not provided.

# dir_diary\mapper.py
2023-09-12 11:21:54
To use this code, follow these instructions:

1. Import the necessary modules:
   - `os`
   - `pathspec`
   - `Path` from `pathlib`
   - `datetime`
   - `ProjectFile` from `file_handler` (assuming it is imported from a separate module called `file_handler.py`)

2. To create a list of `ProjectFile` objects that represent the files in a project folder, use the `map_project_folder` function.
   - Optionally, provide the `startpath` argument to specify the path to the project folder. If no argument is provided, the current directory will be used.
   - The function returns a list of `ProjectFile` objects.

Example usage:
```python
project_files = map_project_folder(startpath="path/to/project/folder")
```

3. To remove files that are ignored by the .gitignore files in a project, use the `remove_gitignored_files` function.
   - Optionally, provide the `startpath` argument to specify the path to the project folder. If no argument is provided, the current directory will be used.
   - The function also expects a list of `ProjectFile` objects called `project_files` as an argument. This list represents all the files in the project.
   - The function returns a filtered list of `ProjectFile` objects that do not match any patterns in the .gitignore files.

Example usage:
```python
filtered_files = remove_gitignored_files(startpath="path/to/project/folder", project_files=project_files)
```

4. To access the `path` and `modified` attributes of a `ProjectFile` object, use the dot notation.
   - `ProjectFile.path` returns the path of the file as a `Path` object.
   - `ProjectFile.modified` returns the modified timestamp of the file as a formatted string ("%Y-%m-%d %H:%M:%S").

Example usage:
```python
for file in project_files:
    print(file.path, file.modified)
```

Note: Uncertainties regarding the expected data types and imports are flagged in the code as comments. Additional information, such as the content of the `file_handler` module, would be required to provide more specific instructions.

# dir_diary\openai_chatbot.py
2023-09-16 16:01:03
To use the code, follow these instructions:

1. Import the following modules:
   - `FileClassificationList` from the `datastructures` module.
   - `LLMClient` from the `client` module.
   - `Optional` and `Literal` from the `typing` module.
   - `openai` (uncertainty about where it is imported from).
   - `models` from the `llm_cost_estimation` module.

2. Define a list of functions with the following structure:
   - Each function dictionary should have the following keys:
     - "name": Name of the function.
     - "description": Description of the function.
     - "parameters": Use the `FileClassificationList.model_json_schema()` method to get the expected data structure for the parameters.

3. Define a string variable `file_classification_prompt` that represents a template for mapping the file structure of a project folder.

4. Define a function named `classify_with_openai` that takes a `project_map` as input, which is an instance of `FileClassificationList`. The function returns an instance of `FileClassificationList`.

5. Inside the `classify_with_openai` function:
   - Convert the `project_map` to an input string by iterating over the `files` attribute of `project_map` and extracting the `path` of each file.
   - Query the LLM (uncertainty about what this is) by calling the `query_llm` function with the `file_classification_prompt` and the `functions` list.
   - Retrieve the project map from the response.
   - Create a new instance of `FileClassificationList` by validating the JSON project map obtained from the response.
   - Return the parsed project map.

6. Define a string variable `pseudocode_prompt` that represents a template for generating a pseudocode summary of a code module.

7. Define a string variable `usage_prompt` that represents a template for generating a usage summary of a code module.

8. Define a function named `summarize_with_openai` that takes an `input_str` as a string and a `summary_type` as a string literal with possible values of "pseudocode" or "usage". The function returns a string.

9. Inside the `summarize_with_openai` function:
   - Determine the appropriate prompt based on the `summary_type`.
   - Query the chatbot by calling the `query_llm` function with the determined prompt and the `input_str`.
   - Retrieve the generated summary from the response.
   - Return the generated summary.

10. Define a function named `get_max_tokens` that takes an optional boolean argument `long`. The function returns an integer.

11. Inside the `get_max_tokens` function:
    - Initialize an instance of `LLMClient`.
    - Set the `model_name` variable based on the `client.model_name` or `client.long_context_fallback` values, depending on the `long` argument.
    - Set the `max_tokens` variable based on the `model_name`. The value will be 16000 if "32k" is in the model_name, 8000 if "16k" is in the model_name, 4000 if "gpt-4" is in the model_name, and 2000 otherwise.
    - Return the `max_tokens`.

12. Define a function named `query_llm` that takes a `prompt` as a string and an optional `functions` list as a parameter. The function returns a string.

13. Inside the `query_llm` function:
    - Initialize an instance of `LLMClient`.
    - Set the `openai.api_key` to the `client.api_key` value.
    - Prepare the common arguments for the API request, including the model name, messages (with the user role and content), and the `max_tokens` value obtained from the `get_max_tokens` function.
    - If `functions` is provided, add it to the request arguments along with the first function name.
    - Generate the output by calling the `openai.ChatCompletion.create` function with the prepared request arguments.
    - Update the total cost by calling the `calculate_cost` function.
    - Return the response object.

14. Define a function named `calculate_cost` that takes a `response` dictionary as input and returns a float.

15. Inside the `calculate_cost` function:
    - Extract the `prompt_tokens`, `completion_tokens`, and `model_used` from the `response` dictionary.
    - Get the cost per token for the used model from the `models` object (uncertainty about the origin of this object).
    - Parse the cost per token strings by splitting them using the " / " separator and converting the numerator and denominator to floats.
    - Calculate and return the total cost of the query by multiplying the prompt tokens with the prompt cost per token and the completion tokens with the completion cost per token.

16. Define a function named `parse_and_calculate` that takes a `cost_str` as a string and returns a float.

17. Inside the `parse_and_calculate` function:
    - Split the `cost_str` using the " / " separator to obtain the numerator and denominator strings.
    - Convert the numerator and denominator strings to floats.
    - Calculate and return the division result.

Note: The usage of the imported functions and classes from outside this module is uncertain and should be flagged at the respective places in the instructions.

# dir_diary\summarize.py
2023-09-16 16:30:48
To use this code, you will need to import the following modules:
- `LLMClient` from the `client` module
- `classify_files` from the `classifier` module
- `summarize_file` from the `summarizer` module
- `read_summary_file`, `write_summary_file`, `identify_new_and_modified_files`, `remove_deleted_files_from_summaries`, `ModuleSummary`, and `ProjectFile` from the `file_handler` module
- `map_project_folder` and `remove_gitignored_files` from the `mapper` module
- `ALLOWED_SUMMARY_TYPES`, `ALLOWED_ROLES`, `ALLOWED_MODELS`, and `ALLOWED_FALLBACKS` from the `datastructures` module
- `validate_literals` and `validate_paths` from the `validators` module
- `Path` from the `pathlib` module
- `PathLike` from the `os` module
- `Union` and `Literal` from the `typing` module

To create an instance of the `LLMClient` class, use the following code:
```
client = LLMClient(api_key=api_key, model_name=model_name, long_context_fallback=long_context_fallback, temperature=temperature, total_cost=0)
```
- `api_key` (str): The API key for the chatbot.
- `model_name` (Literal[str]): The name of the chatbot model to use. Must be one of the allowed models: "gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613".
- `long_context_fallback` (Literal[str]): The fallback model to use for long conversations. Must be one of the allowed fallbacks: 'gpt-4', 'gpt-4-0314', 'gpt-4-0613', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613'.
- `temperature` (float): The temperature value for generating responses.

To invoke the `map_project_folder` function, use the following code:
```
project_files = map_project_folder(startpath=startpath)
```
- `startpath` (Union[str, PathLike]): The path to the project folder to be summarized.

To invoke the `remove_gitignored_files` function, use the following code:
```
project_files = remove_gitignored_files(startpath=startpath, project_files=project_files)
```
- `startpath` (Union[str, PathLike]): The path to the project folder.
- `project_files` (list[ProjectFile]): The list of `ProjectFile` objects representing the files in the project folder.

To invoke the `classify_files` function, use the following code:
```
project_files = classify_files(project_map_file=project_map_file, project_files=project_files)
```
- `project_map_file` (Path): The path to the project map file.
- `project_files` (list[ProjectFile]): The list of `ProjectFile` objects representing the files in the project folder.

To invoke the `remove_deleted_files_from_summaries` function, use the following code:
```
updated_summaries = remove_deleted_files_from_summaries(summaries=summaries, files=project_files)
```
- `summaries` (list[ModuleSummary]): The list of `ModuleSummary` objects representing the existing summaries.
- `files` (list[ProjectFile]): The list of `ProjectFile` objects representing the files in the project folder.

To invoke the `identify_new_and_modified_files` function, use the following code:
```
new_files, modified_files = identify_new_and_modified_files(summaries=summaries, project_files=project_files)
```
- `summaries` (list[ModuleSummary]): The list of `ModuleSummary` objects representing the existing summaries.
- `project_files` (list[ProjectFile]): The list of `ProjectFile` objects representing the files in the project folder.

To invoke the `summarize_file` function, use the following code:
```
generated_summaries = summarize_file(file_to_summarize=file, summary_type=type)
```
- `file_to_summarize` (ProjectFile): The `ProjectFile` object representing the file to be summarized.
- `summary_type` (str): The type of summary to generate.

To invoke the `read_summary_file` function, use the following code:
```
summaries = read_summary_file(summary_file=file_path)
```
- `summary_file` (Path): The path to the summary file.

To invoke the `write_summary_file` function, use the following code:
```
write_summary_file(summaries=updated_summaries, summary_file=file_path)
```
- `summaries` (list[ModuleSummary]): The list of `ModuleSummary` objects representing the updated summaries.
- `summary_file` (Path): The path to the summary file.

To invoke the `validate_literals` function, use the following code:
```
validate_literals(arguments=[{'var_name': 'summary_types', 'allowed_set': ALLOWED_SUMMARY_TYPES, 'value': summary_types}, {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': include}, {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': model_name}, {'var_name': 'long_context_fallback', 'allowed_set': ALLOWED_FALLBACKS, 'value': long_context_fallback}])
```
- `arguments` (list[dict]): The list of dictionaries containing variable name, allowed set, and value.

To invoke the `validate_paths` function, use the following code:
```
startpath, destination = validate_paths(startpath=startpath, destination=destination)
```
- `startpath` (Union[str, PathLike]): The path to the project folder.
- `destination` (Union[str, PathLike]): The path to the destination folder.

To use the `summarize_project_folder` function, call it with the desired arguments:
```
summarize_project_folder(startpath='path/to/project_folder/', destination='path/to/destination_folder/', summary_types=['pseudocode'], include=['source'], api_key='your_api_key', model_name='gpt-3.5-turbo', long_context_fallback='gpt-3.5-turbo-16k', temperature=0)
```
- `startpath` (Union[str, PathLike], optional): The path to the project folder to be summarized. Default is the current directory.
- `destination` (Union[str, PathLike], optional): The path to the destination folder where the summary files will be created. Default is a folder named "docs" in the current directory.
- `summary_types` (Union[tuple, list[Literal["pseudocode", "usage", "tech stack"]]], optional): The types of summaries to generate. Default is ["pseudocode"].
- `include` (Union[tuple, list[Literal["source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", "specialized"]]], optional): The roles of files to include in the summaries. Default is ["source", "utility scripts"].
- `api_key` (str, optional): The API key for the chatbot. Default is None.
- `model_name` (Literal[str], optional): The name of the chatbot model to use. Must be one of the allowed models. Default is "gpt-3.5-turbo".
- `long_context_fallback` (Literal[str], optional): The fallback model to use for long conversations. Must be one of the allowed fallbacks. Default is "gpt-3.5-turbo-16k".
- `temperature` (float, optional): The temperature value for generating responses. Default is 0.

# dir_diary\summarizer.py
2023-09-16 16:18:39
To use the provided code, follow these instructions:

1. Import the following modules and classes:
   - `Literal` from the `typing` module.
   - `ModuleSummary`, `ProjectFile` from the `file_handler` module.
   - `summarize_with_openai` from the `openai_chatbot` module. Note: the location of these modules is not specified in the code, so make sure they are accessible in the same directory or specify the correct import path.

2. To generate a pseudocode or usage summary of a module file, use the `summarize_file` function. It takes two arguments:
   - `file_to_summarize`: A `ProjectFile` object representing the file you want to summarize. Create an instance of `ProjectFile` and pass it as this argument. The `ProjectFile` class might come from the `file_handler` module.
   - `summary_type`: A string literal specifying the type of summary you want. It can be either "pseudocode" or "usage".

3. The `summarize_file` function returns a `ModuleSummary` object, which represents the generated summary. You can access the summary by accessing the `content` attribute of the returned `ModuleSummary` object.

4. If any line in the generated summary starts with a hashtag (#), it is important to remove it and wrap the line with double asterisks (**). This is because hashtags might break file parsing. The code already handles this internally.

5. To replace hashtags in a text, use the `replace_hashtags` function. Pass the text as a string to this function. It returns the cleaned text with hashtags replaced.

Here is an example usage of the code:

```python
from typing import Literal
from .file_handler import ModuleSummary, ProjectFile
from .openai_chatbot import summarize_with_openai

**Create a ProjectFile instance representing the module file to summarize**
file_to_summarize = ProjectFile(path="path/to/module_file.py", modified=True)

**Specify the type of summary you want**
summary_type = "pseudocode"

**Generate the summary using the summarize_file function**
module_summary = summarize_file(file_to_summarize, summary_type)

**Access the generated summary**
generated_summary = module_summary.content

**Print the generated summary**
print(generated_summary)
```

# dir_diary\validators.py
2023-09-15 14:04:24
Instructions for using the code:

1. Creating an instance of the `disable_exception_traceback` context manager:
   - To create an instance of the `disable_exception_traceback` context manager, use the `with` statement.
   - Wrap the code that you want to disable the traceback for inside the `with` block.
   - After the `with` block, the traceback information will be suppressed.
   Example:
   ```
   with disable_exception_traceback():
       # Code with disabled traceback
   ```

2. Invoking the `validate_literal` function:
   - Call the `validate_literal` function and provide the following arguments:
     - `value`: The value to be validated.
     - `allowed_set`: A set of allowed values that `value` can be.
     - `var_name`: The name of the variable being validated.
   - The function will raise a `ValueError` if `value` is not in the `allowed_set`.
   Example:
   ```
   validate_literal(value=5, allowed_set={1, 2, 3}, var_name="my_var")
   ```

3. Invoking the `validate_literals` function:
   - Call the `validate_literals` function and provide a list of dictionaries as the `arguments` argument.
     - Each dictionary represents an argument to be validated and should contain the keys `'var_name'`, `'allowed_set'`, and `'value'`.
     - `'var_name'` should be a string representing the name of the variable being validated.
     - `'allowed_set'` should be a set of allowed values that the argument can take.
     - `'value'` should be the value to be validated.
   - The function will iterate over the `arguments` list and call `validate_literal` for each argument.
   - If an argument's `'value'` is a list or tuple, the function will call `validate_literal` for each value in the list or tuple.
   Example:
   ```
   validate_literals(arguments=[
       {'var_name': 'var1', 'allowed_set': {1, 2, 3}, 'value': 2},
       {'var_name': 'var2', 'allowed_set': {'a', 'b', 'c'}, 'value': ['a', 'd', 'c']}
   ])
   ```

4. Invoking the `validate_paths` function:
   - Call the `validate_paths` function and provide the following arguments:
     - `startpath`: The string or `Path` object representing the starting path.
     - `destination`: The string or `Path` object representing the destination path.
   - The function will perform the following validations:
     - Check if both `startpath` and `destination` are instances of either a string or `PathLike` object.
     - Convert `startpath` to a `Path` object for easier manipulation.
     - Check if the current user has read permission for the `startpath`.
     - Check if the current user has write permission for the `destination`.
   - If any of the validations fail, the function will raise a `TypeError` or `PermissionError`.
   - If all validations pass, the function will return a tuple containing the `startpath` and `destination` as `Path` objects.
   Example:
   ```
   start, dest = validate_paths(startpath="/path/to/start", destination="path/to/destination")
   ```

5. Invoking the `validate_temperature` function:
   - Call the `validate_temperature` function and provide the `temperature` argument.
   - The `temperature` argument can be of type `int`, `float`, or `str`.
   - The function will try to convert the `temperature` argument to a `float` first.
   - If the conversion fails, a `ValueError` will be raised.
   - If the conversion is successful, the function will check if the `float_temperature` is an `int`.
   - If `float_temperature` is an `int`, it will be returned as an `int`.
   - Otherwise, the function will check if `float_temperature` is within the range of 0 and 1.
   - If it is within the range, `float_temperature` will be returned as a `float`.
   - If it is not within the range, a `ValueError` will be raised.
   Example:
   ```
   validated_temperature = validate_temperature(0.5)
   ```

6. Invoking the `validate_api_key` function:
   - Call the `validate_api_key` function and provide the `api_key` argument as a string.
   - The function will validate the `api_key` by calling `openai.Model.list(api_key=api_key)`.
   - If the authentication is successful, "Authentication was successful" will be printed.
   - If the authentication fails, an `openai.OpenAIError` will be raised.
   - To suppress the traceback, the function uses the `disable_exception_traceback` context manager.
   - If an error occurs during the authentication, the function will raise the error with the traceback disabled.
   - If the authentication is successful, the `api_key` will be returned as a string.
   Example:
   ```
   validated_api_key = validate_api_key("my_api_key")
   ```

# dir_diary\__init__.py
2023-09-13 16:53:55
To use the code provided, please follow the instructions below:

1. Import the necessary modules and classes by adding the following line at the top of your script:
   ```
   from __init__ import summarize_project_folder, read_summary_file, ModuleSummary
   ```

2. To summarize a project folder, use the `summarize_project_folder` function. This function takes a single argument, which is the path to the project folder. The summary will be printed to the console. Here is an example usage:
   ```
   summarize_project_folder('/path/to/project/folder')
   ```

3. To read a summary file, use the `read_summary_file` function. This function takes a single argument, which is the path to the summary file. It returns the contents of the file as a string. Here is an example usage:
   ```
   summary = read_summary_file('/path/to/summary/file')
   ```

4. The `ModuleSummary` class can be used to create instances representing summary files for individual modules within a project. To create an instance, use the class constructor and provide the path to the module's summary file as an argument. Here is an example usage:
   ```
   module_summary = ModuleSummary('/path/to/module/summary/file')
   ```

   Once you have an instance of `ModuleSummary`, you can access its attributes and invoke its methods. The available attributes and methods are not specified in the provided code, so it's uncertain what data types are expected or returned. Please refer to the documentation or code implementation of the `ModuleSummary` class to determine its usage.

