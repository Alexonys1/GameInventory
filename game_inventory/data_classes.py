from typing import NamedTuple, Any
from dataclasses import dataclass, field
from enum import StrEnum


class InventoryCell(NamedTuple):
    cell_number: int
    item: Any


class NumerationModesForInventory(StrEnum):
    BY_ROWS = "BY_ROWS"
    BY_COLUMNS = "BY_COLUMNS"


@dataclass
class Item:
    amount: int
    max_stack: int = field(init=False)


@dataclass
class Sextant(Item):
    max_size: int = 10
