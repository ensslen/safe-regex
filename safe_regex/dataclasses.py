import pydantic


class SafeRegexAbstractModel(pydantic.BaseModel):
    class Config:
        extra = "forbid"


class SafeRegex(SafeRegexAbstractModel):
    unique_list: pydantic.conset(item_type=str)