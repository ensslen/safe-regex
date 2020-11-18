from safe_regex.dataclasses import SafeRegex
import pytest
import pydantic


def test_dataclass():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        SafeRegex(cats=1, unique_list=["a"])


def test_unique_list():
    sr = SafeRegex(unique_list=[1, 1])
    pass