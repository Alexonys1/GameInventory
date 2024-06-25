from abc import ABC, abstractmethod
from pydantic import validate_call
from collections.abc import Callable
from typing import Final

from .data_classes import InventoryCell, NumerationModesForInventory
from .exceptions import ItemNotFound, CellNumberOutOfRange


class Inventory[T](ABC):
    @validate_call
    def __init__(
            self,
            *,
            rows: int,
            columns: int,
            numeration_mode: NumerationModesForInventory,
            default_factory: Callable[[], T] = lambda: None,
    ):
        self._rows: Final[int] = rows
        self._columns: Final[int] = columns
        self._numeration_mode: Final[str] = numeration_mode
        self._all_cells: Final[dict[int, T]] = {
            num: default_factory()
            for num in range(1, rows * columns + 1)
        }
        self._default_item: Final[T] = default_factory()
        self.__post_init__()

    def __len__(self):
        return len(self._all_cells)

    def __repr__(self):
        result = f"{self.__class__.__name__}[\n"
        rows = [list() for _ in range(self._rows)]
        match self._numeration_mode:
            case NumerationModesForInventory.BY_COLUMNS:
                row_number = 0
                for key, value in self._all_cells.items():
                    rows[row_number].append(value)
                    row_number += 1
                    if row_number >= self._rows:
                        row_number = 0

            case NumerationModesForInventory.BY_ROWS:
                row_number = 0
                column_number = 0
                for key, value in self._all_cells.items():
                    rows[row_number].append(value)
                    column_number += 1
                    if column_number >= self._columns:
                        row_number += 1
                        column_number = 0

            case _:
                raise ValueError

        for row in rows: result += str(row) + '\n'
        return result + ']'

    def __post_init__(self) -> None:
        """Метод, выполняющийся после инициализации."""

    @validate_call
    def set(self, cell_number: int, item: T) -> None:
        self._on_set()
        if 1 <= cell_number <= len(self._all_cells):
            self._all_cells[cell_number] = item
        else:
            raise CellNumberOutOfRange(cell_number, len(self._all_cells))

    @validate_call
    def get(self, cell_number: int) -> T:
        self._on_get()
        if 1 <= cell_number <= len(self._all_cells):
            return self._all_cells[cell_number]
        else:
            raise CellNumberOutOfRange(cell_number, len(self._all_cells))

    @validate_call
    def get_first_found_item(self, item: T) -> InventoryCell:
        self._on_get()
        for key, value in self._all_cells.items():
            if self._all_cells[key] == item:
                return InventoryCell(cell_number=key, item=value)
        raise ItemNotFound(item)

    @validate_call
    def get_last_found_item(self, item: T) -> InventoryCell:
        self._on_get()
        for key, value in reversed(self._all_cells.items()):
            if self._all_cells[key] == item:
                return InventoryCell(cell_number=key, item=value)
        raise ItemNotFound(item)

    @validate_call
    def set_into_first_found_empty_cell(self, item: T) -> None:
        self._on_set()
        for key, value in self._all_cells.items():
            if value == self._default_item:
                self._all_cells[key] = item
                break

    @validate_call
    def what_contains(self, cell_number: int) -> T:
        if 1 <= cell_number <= len(self._all_cells):
            return self._all_cells[cell_number]
        else:
            raise CellNumberOutOfRange(cell_number, len(self._all_cells))

    @abstractmethod
    def _on_set(self) -> None:
        """The action to be performed on setting."""

    @abstractmethod
    def _on_get(self) -> None:
        """The action to be performed on getting."""
