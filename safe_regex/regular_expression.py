import pydantic
import os
import yaml
import re
from string import Template


@pydantic.dataclasses.dataclass()
class RegularExpression:
    pattern: pydantic.constr(min_length=2)
    description: pydantic.constr(min_length=3)
    matching_texts: pydantic.conset(item_type=str)
    non_matching_texts: pydantic.conset(item_type=str)

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
        msg = Template(f"$text $verb not match {self.pattern} {self.get_regexr_debug_link()}")
        for text in self.matching_texts:
            assert (
                isinstance(self.match(text), re.Match),
                msg.safe_substitute(text=text, verb="does"),
            )
        for text in self.non_matching_texts:
            assert self.match(text) is None, msg.safe_substitute(text=text, verb="should")

    def get_regexr_debug_link(self) -> str:
        import urllib.parse

        tests = "These should all match\n{}\nNone of these should match\n{}".format(
            "\n".join(sorted(self.matching_texts)), "\n".join(sorted(self.non_matching_texts))
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
