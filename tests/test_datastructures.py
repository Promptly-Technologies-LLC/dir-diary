import click
from typing import get_type_hints
from dir_diary.cli import cli
from dir_diary.summarize import summarize_project_folder
from dir_diary.datastructures import ALLOWED_SUMMARY_TYPES, ALLOWED_ROLES, ALLOWED_MODELS, ALLOWED_FALLBACKS, ProjectFile, FileClassification


# Test that the Literal values in FileClassification match the allowed roles
def test_FileClassification_literals_match_allowed_roles() -> None:
    # Extract the Literal values from FileClassification, excluding NoneType
    literal_values = FileClassification.__annotations__['role'].__args__[0].__args__
    
    # Check if they match the allowed roles
    assert set(literal_values) == ALLOWED_ROLES, f"The Literal values in FileClassification do not match the allowed roles. Literal: {list(literal_values)}, Allowed: {list(ALLOWED_ROLES)}"


# Test that the Literal values in ProjectFile match the allowed roles
def test_ProjectFile_literals_match_allowed_roles() -> None:
    # Extract the Literal values from ProjectFile, excluding NoneType
    literal_values = ProjectFile.__annotations__['role'].__args__[0].__args__
    
    # Check if they match the allowed roles
    assert set(literal_values) == ALLOWED_ROLES, f"The Literal values in ProjectFile do not match the allowed roles. Literal: {list(literal_values)}, Allowed: {list(ALLOWED_ROLES)}"


def test_summarize_project_folder_type_hints() -> None:
    # Get type hints from the function
    type_hints = get_type_hints(obj=summarize_project_folder)

    # Function to extract Literal values from a Union type hint
    def extract_literal_values(union_hint) -> list:
        for arg in union_hint.__args__:
            if hasattr(arg, "__origin__") and arg.__origin__ is list:
                return [val for val in arg.__args__[0].__args__]
        return []

    # Extract the Literal values
    summary_types_literal_values = extract_literal_values(union_hint=type_hints['summary_types'])
    include_literal_values = extract_literal_values(union_hint=type_hints['include'])
    model_name_literal_values = [val for val in type_hints['model_name'].__args__]
    long_context_fallback_literal_values = [val for val in type_hints['long_context_fallback'].__args__]

    # Check if they match the allowed roles and models
    assert set(summary_types_literal_values) == ALLOWED_SUMMARY_TYPES, f"The Literal values for 'summary_types' do not match the allowed summary types. Literal: {summary_types_literal_values}, Allowed: {list(ALLOWED_SUMMARY_TYPES)}"
    assert set(include_literal_values) == ALLOWED_ROLES, f"The Literal values for 'include' do not match the allowed roles. Literal: {include_literal_values}, Allowed: {list(ALLOWED_ROLES)}"
    assert set(model_name_literal_values) == ALLOWED_MODELS, f"The Literal values for 'model_name' do not match the allowed models. Literal: {model_name_literal_values}, Allowed: {list(ALLOWED_MODELS)}"
    assert set(long_context_fallback_literal_values) == ALLOWED_FALLBACKS, f"The Literal values for 'long_context_fallback' do not match the allowed models. Literal: {long_context_fallback_literal_values}, Allowed: {list(ALLOWED_FALLBACKS)}"


def test_click_options_match_allowed_options() -> None:
    # Loop through each Click option in the command object
    for param in cli.params:
        if isinstance(param, click.Option):
            # Extract the name and choices for each option
            name = param.name
            choices = param.type.choices if param.type and hasattr(param.type, 'choices') else None
            
            # Compare the choices to the allowed sets
            if name == 'summary_types':
                assert set(choices) == ALLOWED_SUMMARY_TYPES, f"The choices for '{name}' in the Click command do not match the allowed summary types. Choices: {choices}, Allowed: {list(ALLOWED_SUMMARY_TYPES)}"
            elif name == 'include':
                assert set(choices) == ALLOWED_ROLES, f"The choices for '{name}' in the Click command do not match the allowed roles. Choices: {choices}, Allowed: {list(ALLOWED_ROLES)}"
            elif name == 'model_name':
                assert set(choices) == ALLOWED_MODELS, f"The choices for '{name}' in the Click command do not match the allowed models. Choices: {choices}, Allowed: {list(ALLOWED_MODELS)}"
            elif name == 'long_context_fallback':
                assert set(choices) == ALLOWED_FALLBACKS, f"The choices for '{name}' in the Click command do not match the allowed models. Choices: {choices}, Allowed: {list(ALLOWED_FALLBACKS)}"
