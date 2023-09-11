import pytest
from typing import get_type_hints
from pseudocode_summarizer.summarize import summarize_project_folder
from pseudocode_summarizer.datastructures import ALLOWED_ROLES, ALLOWED_MODELS, ProjectFile, FileClassification, validate_value, validate_arguments


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

    # Extract the Literal values for 'include', 'model_name', and 'long_context_fallback'
    include_literal_values = [val for val in type_hints['include'].__args__[0].__args__]
    model_name_literal_values = [val for val in type_hints['model_name'].__args__]
    long_context_fallback_literal_values = [val for val in type_hints['long_context_fallback'].__args__]

    # Check if they match the allowed roles and models
    assert set(include_literal_values) == ALLOWED_ROLES, f"The Literal values for 'include' do not match the allowed roles. Literal: {include_literal_values}, Allowed: {list(ALLOWED_ROLES)}"
    assert set(model_name_literal_values) == ALLOWED_MODELS, f"The Literal values for 'model_name' do not match the allowed models. Literal: {model_name_literal_values}, Allowed: {list(ALLOWED_MODELS)}"
    assert set(long_context_fallback_literal_values).issubset(ALLOWED_MODELS), f"The Literal values for 'long_context_fallback' are not a subset of the allowed models. Literal: {long_context_fallback_literal_values}, Allowed: {list(ALLOWED_MODELS)}"


# Test validate_value function
def test_validate_value() -> None:
    # Test with valid role
    validate_value(value="source", allowed_set=ALLOWED_ROLES, var_name="include")

    # Test with invalid role
    with pytest.raises(expected_exception=ValueError):
        validate_value(value="invalid_role", allowed_set=ALLOWED_ROLES, var_name="include")

    # Test with valid model
    validate_value(value="gpt-3.5-turbo", allowed_set=ALLOWED_MODELS, var_name="model_name")

    # Test with invalid model
    with pytest.raises(expected_exception=ValueError):
        validate_value(value="invalid_model", allowed_set=ALLOWED_MODELS, var_name="model_name")

# Test validate_arguments function
def test_validate_arguments() -> None:
    # Test with valid arguments
    validate_arguments(arguments=[
        {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': ['source', 'utility scripts']},
        {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': 'gpt-3.5-turbo'}
    ])

    # Test with invalid role value
    with pytest.raises(expected_exception=ValueError):
        validate_arguments(arguments=[
            {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': ['source', 'invalid_role']}
        ])

    # Test with invalid model value
    with pytest.raises(expected_exception=ValueError):
        validate_arguments(arguments=[
            {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': 'invalid_model'}
        ])

    # Test with both valid and invalid values
    with pytest.raises(expected_exception=ValueError):
        validate_arguments(arguments=[
            {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': ['source', 'utility scripts']},
            {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': 'invalid_model'}
        ])