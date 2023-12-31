# dir-diary

## Overview

`dir-diary` is a Python library and CLI tool for using LLMs to generate a pseudocode summary and/or summary usage instructions for your entire software project folder. This summary can serve as an intermediate step for development, translation, documentation-writing, or embedding for Q&A. The tool leverages GPT-3.5 Turbo to summarize a decent-sized project for just 2-4 cents. `dir-diary` can be used from the command line, in a Python script, or in an automated cloud deployment workflow via Github Actions (see our custom [setup-dir-diary](https://github.com/Promptly-Technologies-LLC/setup-dir-diary) action and [example workflow](https://github.com/Promptly-Technologies-LLC/setup-dir-diary/blob/main/.github/example_workflows/summarize.yml)).

## Installation

If you install `dir-diary` via `pip`, the tool should install and be added to your system PATH. If you install it manually, you may need to manually add it to your PATH.

### PyPi Installation

```bash
pip install -U dir-diary
```

### Clone from GitHub

```bash
git clone https://github.com/Promptly-Technologies-LLC/dir-diary.git
cd dir-diary
pip install .
```

## Usage

### Setting an OpenAI API Key

Setting environment variables for local command-line usage can be done in several ways, depending on your operating system and shell. Here are some methods:

#### 1. Setting a System Environment Variable

If you want to use the `dir-diary` tool frequently on a private system, you may want to set a persistent system environment variable to hold your API key. The method differs depending on your system and shell.

On Linux or MacOS, you can use this Bash command:

```
echo 'export OPENAI_API_KEY=your_api_key_here` >>~/.bash_profile
```

In Windows Powershell, you can set a system environment variable from the command line:

```powershell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY','your_api_key_here')
```

Alternatively, you can set it through the Windows Control Panel:

"Control Panel" > "System" > "Advanced system settings" > "Advanced" > "Environment variables" > "System Variables" > "New"
"Name": OPENAI_API_KEY
"Value":your_api_key_here

#### 2. Exporting a Key for a Single Shell Session

You can set an environment variable for the duration of your shell session, making it available to `dir-diary` in the same session. The exact command differs depending on which shell you use.

In Bash, use the `export` command:

```bash
export OPENAI_API_KEY=your_api_key_here
```

In Windows Command Prompt, you can use the `set` command:

```cmd
set OPENAI_API_KEY=your_api_key_here
```

In Windows PowerShell, you can use the `$env:` prefix:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

#### 3. Using an `.env` File

You can also place your environment variables in a `.env` file in the directory from which you're running the tool:

```
OPENAI_API_KEY=your_api_key_here
```

When you run your script, the tool will automatically load these variables into the environment.

#### Using an option flag

You can also pass your API key as an option flag to the CLI tool (`--api_key="your_openai_api_key"`) or Python API (`api_key="your_openai_api_key"`). For security reasons, this is not recommended, as it will expose your API key in your shell or command-line history.

### Creating a `.gitignore` file

Before running either the Python or CLI tool, make sure to create a `.gitignore` file in your project folder and add any files you want `dir-diary` to ingore in its classification and summarization steps. For instance, if you've placed your OpenAI API key in a `.env` file, you should add `.env` to the `.gitignore` file. By default, the `dir-diary` tool should ignore `.env` anyway. But adding this file to `.gitignore` will help make absolutely certain that your secrets are never exposed through an API call to the LLM or through being included in a summary. The same goes for any other files that may contain sensitive information.

You should also add dependency and environment folders such as `node_modules`. Such folders may have hundreds or thousands of files and will cause summarization to fail due to exceeding context length.

### Using the Tool from the Command-Line Interface

To summarize a project folder, use the `summarize` command in your shell from the folder you want to summarize. The CLI tool will automatically map the project folder, classify files by their role in the project, and generate a pseudocode summary of all project files with the roles you specify for inclusion in the summary. By default, the tool will create a `docs` folder if one does not already exist, and then will create `project_map.json` and `pseudocode.md` files in that folder. The default paths for these files can be adjusted using the `--pseudocode_file` and `--project_map_file` options.

The `project_map.json` file contains a structured representation of the project folder file structure, and the `pseudocode.md` file contains the pseudocode summary of the project as generated by the specified OpenAI model. By default, `dir-diary` uses the GPT-3.5 Turbo model with 8k context length and will fall back to GPT-3.5 Turbo 16k if necessary. The tool currently only supports OpenAI's chat models.

Note that the syntax for setting option flags differs slightly depending on your shell. Bash uses an equal sign, while Windows Powershell and Command Prompt use a space, as in the examples below. Also note that for arguments that can take multiple values, you will need to invoke the option flag separately for each value (as shown here for `--include`).

#### Bash/Zsh

```bash
summarize --startpath="./" --summary_types="pseudocode" --include "source" --include "testing" --api_key="your_openai_api_key"
```

#### PowerShell or Windows CMD

```powershell
summarize --startpath ".\" --summary_types "pseudocode" --include "source" --include "testing" --api_key "your_openai_api_key"
```

#### Option Flags

Option Flags
- `--startpath`: Specifies the path to the project folder you want to summarize. Defaults to the current directory.
- `--destination`: Specifies the destination folder where generated files will be saved. The folder will be created if does not exist in the startpath directory. Defaults to `--destination "docs"`.
- `--summary_types`: Specified the types of summaries to generate. Accepts multiple values. Valid options are: "pseudocode", "tech stack", and "usage instructions". Only "pseudocode" is currently supported. Defaults to `--summary_types "pseudocode"`.
- `--include`: Specifies the types of files to include in the summary based on their roles. Accepts multiple values. Valid options are: "source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", and "specialized". Defaults to `--include "source" --include "utility scripts"`.
- `--api_key`: Your OpenAI API key. An API key is required for the tool to function, but the option flag is not required if you've set the API key as an environment variable.
- `--model_name`: Specifies the OpenAI model to use for generating the summary. Defaults to `--model_name "gpt-3.5-turbo"`. Valid options are: "gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613".
- `--long_context_fallback`: Specifies the fallback OpenAI model to use when the context is too long for the primary model. Defaults to `--long_context_fallback "gpt-3.5-turbo-16k"`. Valid options are: "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613".
- `--temperature`: Sets the "temperature" for the OpenAI model, affecting the randomness of the output. Defaults to `--temperature 0`.

#### Debugging Authentication Errors

I've encountered some langchain authentication errors when running from a local Windows terminal. If you run into this, let me know by opening an issue. The problem doesn't seem to occur in Github Actions runners or if you have a Python virtual environment activated, so you can try activating a venv before using the tool as a workaround.

### Using dir-diary as Part of a CI/CD Pipeline

The `dir-diary` tool is primarily intended to be used in an automation workflow or as part of a CI/CD or automation pipeline. For this purpose, we have released a [Github Action](https://github.com/Promptly-Technologies-LLC/setup-dir-diary) that handles setup of the tool, which can be used like this:

```yaml
- name: Setup Python and dir-diary
      uses: Promptly-Technologies-LLC/setup-dir-diary@v1
      with:
        install-python: 'true'
```

We have also released a complete [example workflow](https://github.com/Promptly-Technologies-LLC/setup-dir-diary/blob/main/.github/example_workflows/summarize.yml) incorporating this setup action that demonstrates how to automate summarizing a repository and pushing the generated files back to the repo. Note that to use this workflow, you will need to create a Github repository secret named OPENAI_API_KEY with your API access key. Create your secret, add the `summarize.yml` workflow to your repository, and edit to your liking.

### Using the Tool from the Python API

Inside a Python script, you can summarize your project folder with the `summarize_project_folder` function, which takes the same arguments as the CLI tool. 

#### Example Usage

To use the tool from a Python script, import and invoke as follows:

```python
from dir_diary import summarize_project_folder

summarize_project_folder(
    startpath="./my_project",
    pseudocode_file="./my_project/docs/pseudocode.md",
    project_map_file="./my_project/docs/project_map.json",
    include=["source", "documentation"],
    api_key="your_api_key_here",
    model_name="gpt-4",
    long_context_fallback="gpt-4-0314",
    temperature=0.7
)
```

This will generate a pseudocode summary of the "my_project" folder, save it to "./my_project/docs/pseudocode.md", and also create a project map in "./my_project/docs/project_map.json".

#### Parameters

- **`startpath` (Union[str, PathLike], default: ".")**:
  The starting path of the project folder you want to summarize. You can provide this as either a string or a `PathLike` object. The default is the current directory (".").
- **`destination` (Union[str, PathLike], default: "docs")**:
  The destination folder where generated files will be saved. The folder will be created if does not exist in the startpath directory. You can provide this as either a string or a `PathLike` object. The default is "docs".
- **`summary_types` (list[Literal], default: ["pseudocode"])**:
  A list specifying which types of summaries to generate. Valid options are: "pseudocode", "tech stack", and "usage instructions". Only "pseudocode" is currently supported. The default is "pseudocode".
- **`include` (list[Literal], default: ["source", "utility scripts"])**:
  A list specifying which types of files to include in the summary. Valid options are: "source", "configuration", "build or deployment", "documentation", "testing", "database", "utility scripts", "assets or data", and "specialized". The default is to include "source" and "utility scripts".
- **`api_key` (str, default: None)**:
  The API key for the language model. If not provided, the function will use the default API key if available.
- **`model_name` (Literal, default: "gpt-3.5-turbo")**:
  The name of the language model to use for generating the summary. Valid options are: "gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", "gpt-4", "gpt-4-0314", "gpt-4-0613".
- **`long_context_fallback` (Literal, default: "gpt-3.5-turbo-16k")**:
  The name of the fallback language model to use when the primary model's token limit is exceeded. Valid options are the same as for `model_name`. Valid options are: "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613".
- **`temperature` (float, default: 0)**:
  The temperature setting for the language model, affecting the randomness of the output. A value of 0 makes the output deterministic, while higher values (up to 1) make it more random.

#### Tools for Working with the Pseudocode Summary File

The Python API also exposes the `read_pseudocode_file` function and the `ModulePseudocode` class, which can be used to read and parse the pseudocode summary file. The `ModulePseudocode` class is a pydantic model that can be used to validate the JSON file and access its contents. It has the attributes `path`, `modified`, and `content`, which correspond to the path of the module, the last modified timestamp of the module, and the pseudocode summary of the module, respectively. The `read_pseudocode_file` function returns a list of `ModulePseudocode` objects, one for each module in the project folder.

```python
from dir-diary import read_pseudocode_file, ModulePseudocode

pseudocode: list[ModulePseudocode] = read_pseudocode_file("./docs/pseudocode.md")
```

## Contributing

We welcome contributions! Feel free to submit pull requests for new features, improvements, or bug fixes. Please make sure to follow best practices and include unit tests using the pytest framework. Before making contributions, please consult the 'Roadmap' section below.

For any issues, please [create an issue on GitHub](https://github.com/Promptly-Technologies-LLC/dir-diary/issues).

## Modules and Key Functions

- `summarize.py`: Orchestrates the summarization of the entire project folder.
- `cli.py`: Defines the command-line interface for the tool.
- `datastructures.py`: Defines classes and validators for working with data.
- `mapper.py`: Maps the project folder.
- `chatbot.py`: Initializes and queries the chatbot model.
- `classifier.py`: Classifies files' roles by querying the chatbot.
- `summarizer.py`: Summarizes individual files by querying the chatbot.
- `file_handler.py`: Handles reading and writing of pseudocode files.
  
For a more detailed understanding, please refer to the source code, inline comments, and, most importantly, [docs\pseudocode.md](docs\pseudocode.md)!

## Roadmap

- [ ] Replace print statements with proper console logs
- [ ] Add console logging to the folder mapping step, and see if we can improve speed for this step
- [ ] Deal with condition where LLM response['choices']['finish_reason'] == 'length' (success code but response exceeds context length)
- [ ] Fix the way we handle exceeding context length (add filtering, splitting)
- [ ] Use `llm_cost_estimation.models` to get max_tokens
- [ ] Make all summarization API calls asynchronous to reduce runtime
- [ ] Add tech stack summarization feature
- [ ] Add a final summarization step to reconcile the individual file summaries?
- [ ] Do some prompt engineering for better outputs, and/or allow user-defined custom prompts
- [ ] Add some preprocessing to pull the right stuff into context during summarization, maybe using universal ctags or abstract syntax tree?
- [ ] Support summarizing at the object level rather than the module level?
- [ ] Add some prompt chaining and/or preprocessing to usage summarization to ensure we only summarize exported objects
- [ ] Add support for LLMs other than OpenAI's chat models
- [ ] Add support for Microsoft Azure OpenAI service to reduce latency/cost
- [ ] Do some YouTube explainers/demos
- [ ] Add more unit tests
