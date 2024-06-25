from pytest import raises, mark
from collections.abc import Callable

from game_inventory import Inventory, InventoryCell, CellNumberOutOfRange
from game_inventory import NumerationModesForInventory


# Пользователь должен будет переопределить
# два метода абстрактного класса.
class InventoryHandler[T](Inventory[T]):
    def __init__(
            self,
            *,
            rows: int = 5,
            columns: int = 12,
            numeration_mode: NumerationModesForInventory = NumerationModesForInventory.BY_COLUMNS,
            default_factory: Callable[[], T] = lambda: None,
    ):
        super().__init__(rows=rows, columns=columns, numeration_mode=numeration_mode, default_factory=default_factory)

    def __post_init__(self):
        self.test_var: str = "POST INIT"  # Добавляю сугубо для теста.

    def _on_set(self) -> None:
        self.test_var = "ON SET"

    def _on_get(self) -> None:
        self.test_var = "ON GET"

    def _del_item_if_necessary(self) -> None:
        pass


# ================== UNIT TESTS ================== #
def test_post_init_of_inventory_handler():
    sut = InventoryHandler()

    assert sut.test_var == "POST INIT"


def test_inventory_handler_len():
    sut = InventoryHandler()

    assert len(sut) == 60


def test_action_on_set():
    sut = InventoryHandler[str | None]()
    sut.set(cell_number=7, item="value")

    assert sut.test_var == "ON SET"


def test_action_on_get():
    sut = InventoryHandler[str | None]()
    sut.set(cell_number=7, item="value")
    result = sut.get(cell_number=7)

    assert sut.test_var == "ON GET"
    assert result == "value"


def test_default_factory_of_inventory_handler():
    sut = InventoryHandler(default_factory=lambda: "value")

    for i in range(1, 61):
        assert sut.get(i) == "value"


def test_get_first_found_item():
    sut = InventoryHandler[str | None]()
    expected = InventoryCell(cell_number=12, item="value")

    sut.set(cell_number=13, item="value")
    sut.set(cell_number=12, item="value")
    sut.set(cell_number=14, item="value")

    assert sut.get_first_found_item("value") == expected


def test_get_last_found_item():
    sut = InventoryHandler[str | None]()
    expected = InventoryCell(cell_number=14, item="value")

    sut.set(cell_number=12, item="value")
    sut.set(cell_number=14, item="value")
    sut.set(cell_number=13, item="value")

    assert sut.get_last_found_item("value") == expected


def test_cell_number_out_of_range_while_setting():
    with raises(CellNumberOutOfRange):
        sut = InventoryHandler[str | None]()

        sut.set(cell_number=100, item="value")


def test_cell_number_out_of_range_while_getting():
    with raises(CellNumberOutOfRange):
        sut = InventoryHandler()

        sut.get(cell_number=100)


def test_set_item_into_first_found_empty_cell():
    sut = InventoryHandler(default_factory=lambda: "default")
    expected = InventoryCell(cell_number=11, item="value")

    for i in range(1, 11):
        sut.set(cell_number=i, item="another")
    sut.set_into_first_found_empty_cell(item="value")

    assert sut.get_first_found_item(item="value") == expected


def test_show_what_contains_cell():
    sut = InventoryHandler[str | None]()
    expected = "value"

    sut.set(cell_number=10, item="value")

    # При вызове item не должен измениться, в отличие от get.
    assert sut.what_contains(cell_number=10) == expected
    assert sut.what_contains(cell_number=10) == expected


@mark.xfail  # FIXME Придумать что-нибудь...
def test_delete_item_after_set_or_get_if_necessary():
    sut = InventoryHandler[int | None]()
    for i in range(1, 21):
        sut.set(cell_number=i, item=8)

    assert False
