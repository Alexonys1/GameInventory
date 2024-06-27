from typing import NamedTuple, Any
from abc import ABC, abstractmethod
from pydantic import validate_call
from enum import StrEnum


class NumerationModesForInventory(StrEnum):
    BY_ROWS = "BY_ROWS"
    BY_COLUMNS = "BY_COLUMNS"


class InventoryCell(NamedTuple):
    cell_number: int
    item: Any


class Point(NamedTuple):
    x: int
    y: int


class InventoryItem(ABC):
    @validate_call
    def __init__(self, amount: int):
        if 0 < amount <= self.max_stack:
            self._amount = amount
        else:
            raise ValueError

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    @validate_call
    def amount(self, amount, /) -> None:
        if 0 <= amount <= self.max_stack:
            self._amount = amount
        else:
            raise ValueError

    @property
    @abstractmethod
    def max_stack(self) -> int:
        pass


class Sextant(InventoryItem):
    @property
    def max_stack(self) -> int:
        return 10


class Compass(InventoryItem):
    @property
    def max_stack(self) -> int:
        return 1


class ChargedCompass(Compass):
    pass
