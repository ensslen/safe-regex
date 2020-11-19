from safe_regex.dataclasses import RegularExpression
import pytest
import pydantic
import yaml
import re


def test_dataclass():
    with pytest.raises(TypeError):
        RegularExpression(cats=1, regex="abc")


@pytest.fixture
def example():
    return RegularExpression.from_yaml("yyyy-mm-dd", folder="./tests")


def test_from_yaml(example):
    # the test fixture does this for us
    pass


def test_testing():
    with open("./tests/yyyy-mm-dd.re.yaml") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
    sr = RegularExpression(**yaml_data)
    sr.test()


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