import pytest
from dir_diary.validators import validate_literal, validate_literals
from dir_diary.datastructures import ALLOWED_SUMMARY_TYPES, ALLOWED_ROLES, ALLOWED_MODELS, ALLOWED_FALLBACKS


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
