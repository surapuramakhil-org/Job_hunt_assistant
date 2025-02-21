from enum import Enum

from attr import dataclass


class TextBoxQuestionType(Enum):
    NUMERIC = "numeric"
    TEXT = "text"

class SelectQuestionType(Enum):
    SINGLE_SELECT = "single_select"
    MULTI_SELECT = "multi_select"

@dataclass
class SelectQuestion:
    question: str
    options: list[str]
    type: SelectQuestionType
    required: bool


@dataclass
class TextBoxQuestion:
    question: str
    type: TextBoxQuestionType
    required: bool
