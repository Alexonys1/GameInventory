from abc import ABC, abstractmethod
from pydantic import validate_call
from collections.abc import Callable

from .data_classes import InventoryCell
from .exceptions import ItemNotFound, CellNumberOutOfRange


class Inventory[T](ABC):
    @validate_call
    def __init__(self, *, rows: int, columns: int, default_factory: Callable[[], T | None] = lambda: None):
        self._rows = rows
        self._columns = columns
        self._all_cells = {
            num: default_factory()
            for num in range(1, rows * columns + 1)
        }
        self._default_item = default_factory()
        self.__post_init__()

    def __len__(self):
        return len(self._all_cells)

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
    def get_first_found_item(self, item: T) -> InventoryCell[int, T]:
        self._on_get()
        for key, value in self._all_cells.items():
            if self._all_cells[key] == item:
                return InventoryCell(cell_number=key, item=value)
        raise ItemNotFound(item)

    @validate_call
    def get_last_found_item(self, item: T) -> InventoryCell[int, T]:
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

    @abstractmethod
    def _on_set(self) -> None:
        """The action to be performed on setting."""

    @abstractmethod
    def _on_get(self) -> None:
        """The action to be performed on getting."""
