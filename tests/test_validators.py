import pytest
from dotenv import load_dotenv
from os import getenv
import sys
import io
import traceback
from dir_diary.validators import validate_literal, validate_literals, validate_api_key, disable_exception_traceback
from dir_diary.datastructures import ALLOWED_SUMMARY_TYPES, ALLOWED_ROLES, ALLOWED_MODELS, ALLOWED_FALLBACKS
from openai import OpenAIError


# Test validate_literal function
def test_validate_literal() -> None:
    # Test with valid role
    validate_literal(value="source", allowed_set=ALLOWED_ROLES, var_name="include")

    # Test with valid list of roles
    validate_literal(value="source", allowed_set=ALLOWED_ROLES, var_name=["include"])

    # Test with valid tuple of roles
    validate_literal(value="source", allowed_set=ALLOWED_ROLES, var_name=("include",))

    # Test with invalid role
    with pytest.raises(expected_exception=ValueError):
        validate_literal(value="invalid_role", allowed_set=ALLOWED_ROLES, var_name="include")

    # Test with valid model
    validate_literal(value="gpt-3.5-turbo", allowed_set=ALLOWED_MODELS, var_name="model_name")

    # Test with invalid model
    with pytest.raises(expected_exception=ValueError):
        validate_literal(value="invalid_model", allowed_set=ALLOWED_MODELS, var_name="model_name")


# Test validate_literals function
def test_validate_literals() -> None:
    # Test with valid arguments
    validate_literals(arguments=[
        {'var_name': 'summary_types', 'allowed_set': ALLOWED_SUMMARY_TYPES, 'value': ['pseudocode']},
        {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': ['source', 'utility scripts']},
        {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': 'gpt-3.5-turbo'},
        {'var_name': 'long_context_fallback', 'allowed_set': ALLOWED_FALLBACKS, 'value': 'gpt-3.5-turbo-16k'}
    ])

    # Test with invalid role value
    with pytest.raises(expected_exception=ValueError):
        validate_literals(arguments=[
            {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': ['source', 'invalid_role']}
        ])

    # Test with invalid model value
    with pytest.raises(expected_exception=ValueError):
        validate_literals(arguments=[
            {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': 'invalid_model'}
        ])

    # Test with both valid and invalid values
    with pytest.raises(expected_exception=ValueError):
        validate_literals(arguments=[
            {'var_name': 'include', 'allowed_set': ALLOWED_ROLES, 'value': ['source', 'utility scripts']},
            {'var_name': 'model_name', 'allowed_set': ALLOWED_MODELS, 'value': 'invalid_model'}
        ])


# Test validate_api_key
def test_validate_api_key() -> None:
    # Test with invalid API key
    invalid_api_key = "invalid_key"
    with pytest.raises(expected_exception=OpenAIError):
        validate_api_key(api_key=invalid_api_key)
    
    # Test with valid API key
    load_dotenv()
    valid_api_key = getenv(key="OPENAI_API_KEY")
    output = validate_api_key(api_key=valid_api_key)

    assert output == valid_api_key


# Test disable_exception_traceback
def test_disable_exception_traceback() -> None:
    # Redirect stderr
    new_stderr = io.StringIO()
    old_stderr = sys.stderr
    sys.stderr = new_stderr

    try:
        with disable_exception_traceback():
            try:
                raise ValueError("This is a test error")
            except Exception:
                traceback.print_exc()
    finally:
        # Reset stderr
        sys.stderr = old_stderr

    error_output = new_stderr.getvalue()
    assert "Traceback" not in error_output
    assert "ValueError: This is a test error" in error_output
