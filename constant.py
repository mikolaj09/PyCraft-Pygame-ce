from dataclasses import dataclass


@dataclass(frozen=True)
class Constant:

    name: str
    value: int
