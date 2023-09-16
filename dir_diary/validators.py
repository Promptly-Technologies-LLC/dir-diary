from typing import Union
from os import PathLike, access, R_OK, W_OK
from pathlib import Path
from contextlib import contextmanager
import sys
import openai


# Raise exception without printing traceback
@contextmanager
def disable_exception_traceback():
    """
    All traceback information is suppressed and only the exception type and value are printed
    """
    default_value = getattr(sys, "tracebacklimit", 1000)
    sys.tracebacklimit = 0
    yield
    sys.tracebacklimit = default_value


# Generic validation function
def validate_literal(value, allowed_set, var_name) -> None:
    if value not in allowed_set:
        raise ValueError(f"The `{var_name}` argument must be one of {allowed_set}")


# Function to validate multiple arguments
def validate_literals(arguments) -> None:
    for arg in arguments:
        var_name = arg['var_name']
        allowed_set = arg['allowed_set']
        value = arg['value']
        if isinstance(value, (list, tuple)):
            for val in value:
                validate_literal(value=val, allowed_set=allowed_set, var_name=var_name)
        else:
            validate_literal(value=value, allowed_set=allowed_set, var_name=var_name)


# Function to validate a path
def validate_paths(startpath: str, destination: str) -> tuple[Path, Path]:
    # Type Check
    if not isinstance(startpath, (str, PathLike)):
        raise TypeError(f"Expected a Path-like object or string for startpath; got {type(startpath)}")
    if not isinstance(destination, (str, PathLike)):
        raise TypeError(f"Expected a Path-like object or string for destination; got {type(destination)}")

    # Convert to Path object for easier manipulation
    startpath = Path(startpath)
    destination = startpath / Path(destination)

    # Permission Checks
    if not access(path=startpath, mode=R_OK):
        raise PermissionError(f"Read permission is required for the startpath {startpath}")

    if not access(path=startpath, mode=W_OK):
        raise PermissionError(f"Write permission is required for the destination path {destination}")
    
    return startpath, destination


def validate_temperature(temperature: Union[int, float, str]) -> Union[int, float]:
    # Try to convert to float first
    try:
        float_temperature = float(temperature)
    except ValueError:
        raise ValueError("The `temperature` argument must be convertible to an int or float.")
    
    # Check if it's actually an int
    if float_temperature.is_integer():
        return int(float_temperature)
    
    # Check the range
    if float_temperature < 0 or float_temperature > 1:
        raise ValueError("The `temperature` argument must be between 0 and 1.")
    
    return float_temperature


def validate_api_key(api_key: str) -> str:
    try:
        openai.Model.list(api_key=api_key)
        print("Authentication was successful")
    except openai.OpenAIError as err:
        with disable_exception_traceback():
            raise(err)

    return api_key
