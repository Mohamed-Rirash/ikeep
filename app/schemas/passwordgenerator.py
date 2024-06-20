from enum import Enum


class PasswordGeneratorRequest(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
