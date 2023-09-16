from .datastructures import FileClassificationList
from .client import LLMClient
from typing import Optional, Literal
import json
import openai
from llm_cost_estimation import models


# Functions to enforce structured output from the chatbot
functions: list[dict] = [
        {
          "name": "classify_project_files_by_role",
          "description": "Identify the role that each file plays in a software project",
          "parameters": FileClassificationList.model_json_schema()
        }
    ]

# Prompt template for determining the roles that files play in the project
file_classification_prompt = (
    "We have mapped the file structure of a project folder for an existing "
    "coding project. Based solely on the file structure, let's attempt to "
    "classify them by the role they play in the project. We will label code "
    "modules, entry points, and endpoints as 'source'; config files, "
    "environment files, and dependency files as 'configuration'; build files, "
    "Docker files, and CI/CD files as 'build or deployment'; READMEs, "
    "CHANGELOGs, pseudocodes, project maps, licenses, and docs as "
    "'documentation'; unit tests as 'testing'; migration, schema, and seed "
    "files as 'database', utility and action scripts as 'utility scripts', "
    "static assets like images, CSS, CSV, and JSON files as 'assets and "
    "data', and anything else that doesn't fit these categories (e.g., "
    "compiled distribution files) as 'specialized'. Every file must be "
    "assigned a valid role. 'None' and 'null' values are not allowed."
    "Economize by returning minified JSON without extraneous whitespace.\n"
    "Here is the map of the project file structure:\n%s"
)

def classify_with_openai(project_map: FileClassificationList) -> FileClassificationList:
    # Convert the project_map to an input string
    input_str: str = ", ".join([str(object=file.path) for file in project_map.files])

    # Query the LLM to update the project map
    print("Prompt: " + file_classification_prompt % input_str)
    response = query_llm(
                prompt=file_classification_prompt % input_str,
                functions=functions
            )

    # Get the project map from the response
    json_project_map: list[dict] = response['choices'][0]['message']['function_call']['arguments']
    print("Output: " + json.dumps(obj=json_project_map))

    # Create a FileClassificationList from the returned JSON project map
    parsed_project_map: FileClassificationList = FileClassificationList.model_validate_json(json_data=json_project_map)

    # Return the project map
    return parsed_project_map


# Prompt to generate a pseudocode summary of a code module
pseudocode_prompt = (
    "Generate an abbreviated natural-language pseudocode summary of the "
    "following code. Make sure to include function, class, and argument names "
    "and to indicate where objects are imported from so a reader can "
    "understand the execution context and usage. Well-formatted pseudocode "
    "will separate object and function blocks with a blank line and will use "
    "hierarchical ordered and unordered lists to show execution sequence and "
    "logical relationships.\nHere is the code to summarize:\n%s"
)

# Prompt to generate a usage summary of a code module
usage_prompt = (
    "Generate natural-language instructions on how to use the following code. "
    "Describe what the code is doing, how to create instances or invoke "
    "methods of defined objects, and how to invoke functions. As much as "
    "possible, infer what data types are expected by function arguments and "
    "class methods, as well as what data types are returned. When usage "
    "cannot be inferred for types and classes imported from outside this "
    "module, flag the uncertainties and indicate where they are imported "
    "from. Well-formatted usage summaries will separate instructions for "
    "different objects and functions with a blank line.\nHere is the code to "
    "summarize:\n%s"
)

def summarize_with_openai(input_str: str, summary_type: Literal["pseudocode", "usage"]) -> str:
    # Determine the prompt to use
    if summary_type == "pseudocode":
        prompt = pseudocode_prompt
    elif summary_type == "usage":
        prompt = usage_prompt

    # Query the chatbot for a summary and parse the output
    print("Prompt: " + prompt % input_str)
    response: dict = query_llm(
                prompt=prompt % input_str
            )
    
    # Get the generated summary from the response
    generated_summary: str = response["choices"][0]["message"]["content"]
    print("Output: " + generated_summary)
    
    return generated_summary


# Get max_tokens based on model_name
def get_max_tokens(long: bool = False) -> int:
    # Initialize LLMClient to get config and track cost
    client = LLMClient()
    
    # Set model_name based on config + `long` argument
    model_name = client.model_name if not long else client.long_context_fallback
    
    # Set max_tokens based on model_name
    if "32k" in model_name:
        max_tokens = 16000
    elif "16k" in model_name:
        max_tokens = 8000
    elif "gpt-4" in model_name:
        max_tokens = 4000
    else:
        max_tokens = 2000

    # Return the chatbot instance
    return max_tokens


# Query a chatbot using a prompt, and optionally a functions list
def query_llm(prompt: str, functions: Optional[list[dict]] = None) -> str:
    # Initialize the client
    client = LLMClient()
    openai.api_key = client.api_key

    # Prepare common arguments
    request_args = {
        'model': client.model_name,
        'messages': [{"role": "user", "content": prompt}],
        'max_tokens': get_max_tokens(long=False),
    }
    if functions is not None:
        request_args['functions'] = functions
        request_args['function_call'] = {'name': functions[0]['name']}

    try:
        # Generate the output from the input
        response: dict = openai.ChatCompletion.create(**request_args)
    except openai.InvalidRequestError as e:
        if client.long_context_fallback is None:
            raise e
        else:
            print(f"Encountered error:\n{e}\nTrying again with long_context_fallback.")
            request_args['model'] = client.long_context_fallback
            request_args['max_tokens'] = get_max_tokens(long=True)
            response: dict = openai.ChatCompletion.create(**request_args)

    # Update the total cost
    client.total_cost += calculate_cost(response=response)

    # Return the response object
    return response


# Calculate cost of a query
def calculate_cost(response: dict) -> float:
    prompt_tokens=response["usage"]["prompt_tokens"]
    completion_tokens=response["usage"]["completion_tokens"]
    model_used = response["model"]
    
    # Get cost per token for the model used from the models object
    prompt_cost_per_token: str = [model['prompt_cost_per_token'] for model in models if model['name'] == model_used][0]
    completion_cost_per_token: str = [model['completion_cost_per_token'] for model in models if model['name'] == model_used][0]
    
    # Parse the cost per token strings
    prompt_cost_per_token = parse_and_calculate(cost_str=prompt_cost_per_token)
    completion_cost_per_token = parse_and_calculate(cost_str=completion_cost_per_token)

    # Calculcate and return the total cost of the query
    total_cost = (prompt_tokens * prompt_cost_per_token) + (completion_tokens * completion_cost_per_token)
    return total_cost


def parse_and_calculate(cost_str: str) -> float:
    num_str, den_str = cost_str.split(sep=" / ")
    return float(num_str) / float(den_str)
