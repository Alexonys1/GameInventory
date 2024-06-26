import inspect

from abc import ABC, abstractmethod
from pydantic import validate_call
from collections.abc import Callable
from functools import wraps
from typing import Final

from loguru import logger as log

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
        self._default_factory: Final[Callable[[], T]] = default_factory
        self._last_used_cell_number: int = 0
        log.debug(f"Создан экземпляр {self}")
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

    @staticmethod
    def _on_set(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            function(self, *args, **kwargs)  # Функция get или set.
            self._do_action_on_set(self._last_used_cell_number)
        return wrapper
    '''
    @staticmethod
    def _setter_with_cell_number_and_item(function):
        @wraps(function)
        def wrapper(self, cell_number: int, item: T):
            self._do_action_on_set(self, cell_number=cell_number, item=item)
            function(self, cell_number, item)  # Функция get или set.
        return wrapper
    '''
    @staticmethod
    def _on_get(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            result = function(self, *args, **kwargs)  # Функция get или set.
            self._do_action_on_get(self._last_used_cell_number)
            return result
        return wrapper

    @validate_call
    @_on_set
    def set(self, cell_number: int, item: T) -> None:
        func_name = inspect.currentframe().f_code.co_name
        log.trace(f"Вызывается метод {func_name}")
        if 1 <= cell_number <= len(self._all_cells):
            log.debug(f"{func_name} записывает в ячейку №{cell_number} {item=}")
            self._all_cells[cell_number] = item
            self._last_used_cell_number = cell_number
        else:
            raise CellNumberOutOfRange(cell_number, len(self._all_cells))

    @validate_call
    @_on_get
    def get(self, cell_number: int) -> T:
        func_name = inspect.currentframe().f_code.co_name
        log.trace(f"Вызывается метод {func_name}")
        if 1 <= cell_number <= len(self._all_cells):
            result = self._all_cells[cell_number]
            log.debug(f"{func_name} возвращает из ячейки №{cell_number} {result}")
            self._last_used_cell_number = cell_number
            return result
        else:
            raise CellNumberOutOfRange(cell_number, len(self._all_cells))

    @validate_call
    @_on_get
    def get_first_found_item(self, item: T) -> InventoryCell:
        func_name = inspect.currentframe().f_code.co_name
        log.trace(f"Вызывается метод {func_name}")
        for key, value in self._all_cells.items():
            if self._all_cells[key] == item:
                result = InventoryCell(cell_number=key, item=value)
                log.debug(f"{func_name} возвращает {result}")
                self._last_used_cell_number = key
                return result
        raise ItemNotFound(item)

    @validate_call
    @_on_get
    def get_last_found_item(self, item: T) -> InventoryCell:
        func_name = inspect.currentframe().f_code.co_name
        log.trace(f"Вызывается метод {func_name}")
        for key, value in reversed(self._all_cells.items()):
            if self._all_cells[key] == item:
                result = InventoryCell(cell_number=key, item=value)
                log.debug(f"{func_name} возвращает {result}")
                self._last_used_cell_number = key
                return result
        raise ItemNotFound(item)

    @validate_call
    @_on_set
    def set_into_first_found_empty_cell(self, item: T) -> None:
        func_name = inspect.currentframe().f_code.co_name
        log.trace(f"Вызывается метод {func_name}")
        for key, value in self._all_cells.items():
            if value == self._default_factory():
                log.debug(f"{func_name} записывает в ячейку №{key} {item=}")
                self._all_cells[key] = item
                self._last_used_cell_number = key
                break

    @validate_call
    def what_contains(self, cell_number: int) -> T:
        func_name = inspect.currentframe().f_code.co_name
        log.trace(f"Вызывается метод {func_name}")
        if 1 <= cell_number <= len(self._all_cells):
            result = self._all_cells[cell_number]
            log.debug(f"{func_name} возвращает из ячейки №{cell_number} {result}")
            self._last_used_cell_number = cell_number
            return result
        else:
            raise CellNumberOutOfRange(cell_number, len(self._all_cells))

    @abstractmethod
    def _do_action_on_set(self, cell_number: int) -> None:
        """The action to be performed on setting."""

    @abstractmethod
    def _do_action_on_get(self, cell_number: int) -> None:
        """The action to be performed on getting."""
