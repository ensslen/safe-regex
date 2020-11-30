from safe_regex import RegularExpression
import pytest
import pydantic
import yaml
import re
import os


def test_dataclass():
    with pytest.raises(TypeError):
        RegularExpression(cats=1, regex="abc")


@pytest.fixture
def example():
    return RegularExpression.from_yaml("yyyy-mm-dd", folder="./tests")


def test_testing():
    regex_directory = "./tests"
    for filename in os.listdir(regex_directory):
        if filename.endswith(".re.yaml"):
            with open(os.path.join(regex_directory, filename)) as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
            sr = RegularExpression(**yaml_data)
            sr.test()


def test_regexr_link(example):
    assert (
        example.get_regexr_debug_link()
        == "https://regexr.com/?expression=%2F%5Cd%7B4%7D-%5Cd%7B2%7D-%5Cd%7B2%7D%2Fgms&text=These+should+all+match%0A1999-12-31%0A2020-01-01%0ANone+of+these+should+match%0A42%0Aclaritycloudworks.com"
    )


def test_search(example):
    assert isinstance(example.search("the date was 2020-11-19", 5), re.Match)


def test_match(example):
    assert isinstance(example.match("1111-11-11 was the date", 0, 15), re.Match)


def test_fullmatch(example):
    assert isinstance(example.fullmatch("1111-11-11 was the date", 0, 10), re.Match)


def test_split(example):
    assert example.split("it started 2020-01-01 and ended 2020-02-02", maxsplit=4) == [
        "it started ",
        " and ended ",
        "",
    ]


def test_findall(example):
    assert example.findall("it started 2020-01-01 and ended 2020-02-02", 6) == [
        "2020-01-01",
        "2020-02-02",
    ]


def test_finditer(example):
    assert list(example.findall("the dates where 2020-02-02, 2020-03-03, and 2020-04-04", 6)) == [
        "2020-02-02",
        "2020-03-03",
        "2020-04-04",
    ]


def test_sub(example):
    assert example.sub("yesterday", "it started 2020-01-01") == "it started yesterday"


def test_subn(example):
    assert example.subn("yesterday", "it started 2020-01-01") == ("it started yesterday", 1)


def test_flags(example):
    assert example.flags == re.UNICODE


def test_groups(example):
    assert example.groups == 0


def test_groupindex(example):
    assert example.groupindex == {}