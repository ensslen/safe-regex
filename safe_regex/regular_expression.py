import pydantic
import os
import yaml
import re
import typing


@pydantic.dataclasses.dataclass(frozen=True, order=True)
class RegexTestCase:
    text: pydantic.constr()
    matches: typing.Optional[typing.List[str]] = None

    def run(self, regex):
        """ evaluate the test case against the pattern """
        actual = regex.match(self.text)
        link = regex.get_regexr_debug_link()
        msg = f"{self.text} match of {regex.pattern} != {self.matches}: {link}"
        if self.matches is None:
            assert actual is None, msg
        elif len(self.matches) == 1:
            assert self.matches[0] == actual.group(0), msg
        else:
            for i in range(len(self.matches)):
                assert self.matches[i] == actual.group(i + 1), msg


@pydantic.dataclasses.dataclass()
class RegularExpression:
    pattern: pydantic.constr(min_length=2)
    description: pydantic.constr(min_length=3)
    test_cases: typing.List[RegexTestCase]

    @classmethod
    def from_yaml(cls, expression_name: str, folder: str = None):
        environment_path = os.environ.get("SAFE_REGEX_PATH")
        if folder:
            working_folder = folder
        elif environment_path:
            working_folder = environment_path
        else:
            working_folder = os.getcwd()
        file_path = os.path.join(working_folder, f"{expression_name}.re.yaml")
        with open(file_path, "r") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
        return cls(**yaml_data)

    def __post_init_post_parse__(self):
        self.regex = re.compile(self.pattern)
        self.flags = self.regex.flags
        self.groups = self.regex.groups
        self.groupindex = self.regex.groupindex

    class Config:
        extra = "forbid"

    def test(self):
        for test_case in self.test_cases:
            test_case.run(self)

    def get_regexr_debug_link(self) -> str:
        import urllib.parse

        match = [tc.text for tc in self.test_cases if tc.matches is not None]
        not_match = [tc.text for tc in self.test_cases if tc.matches is None]
        tests = "These should match\n{}\nThese should not match\n{}".format(
            "\n".join(sorted(match)),
            "\n".join(sorted(not_match)),
        )
        params = {"expression": f"/{self.pattern}/gms", "text": tests}
        encoded_params = urllib.parse.urlencode(params)
        return f"https://regexr.com/?{encoded_params}"

    """
    pass through to re.Pattern
    """

    def search(self, *args, **kwargs):
        return self.regex.search(*args, **kwargs)

    def match(self, *args, **kwargs):
        return self.regex.match(*args, **kwargs)

    def fullmatch(self, *args, **kwargs):
        return self.regex.fullmatch(*args, **kwargs)

    def split(self, *args, **kwargs):
        return self.regex.split(*args, **kwargs)

    def findall(self, *args, **kwargs):
        return self.regex.findall(*args, **kwargs)

    def finditer(self, *args, **kwargs):
        return self.regex.finditer(*args, **kwargs)

    def sub(self, *args, **kwargs):
        return self.regex.sub(*args, **kwargs)

    def subn(self, *args, **kwargs):
        return self.regex.subn(*args, **kwargs)
