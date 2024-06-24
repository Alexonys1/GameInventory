from pytest import raises

from game_inventory import Inventory, InventoryCell, CellNumberOutOfRange


# Пользователь должен будет переопределить
# два метода абстрактного класса.
class InventoryHandler[T](Inventory[T]):
    def __post_init__(self):
        self.test_var: str = "POST INIT"  # Добавляю сугубо для теста.

    def _on_set(self) -> None:
        self.test_var = "ON SET"

    def _on_get(self) -> None:
        self.test_var = "ON GET"


def test_post_init_of_inventory_handler():
    sut = InventoryHandler(rows=5, columns=12)

    assert sut.test_var == "POST INIT"


def test_inventory_handler_len():
    sut = InventoryHandler(rows=5, columns=12)

    assert len(sut) == 60


def test_action_on_set():
    sut = InventoryHandler(rows=10, columns=10)
    sut.set(cell_number=7, item="str")

    assert sut.test_var == "ON SET"


def test_action_on_get_and_creating_default_factory():
    sut = InventoryHandler(
        rows=10,
        columns=10,
        default_factory=lambda: 11
    )
    result = sut.get(cell_number=7)

    assert sut.test_var == "ON GET"
    assert result == 11


def test_default_factory_of_inventory_handler():
    sut = InventoryHandler(
        rows=5,
        columns=12,
        default_factory=lambda: "My value"
    )

    assert sut.get(1) == "My value"
    assert sut.get(12) == "My value"
    assert sut.get(60) == "My value"


def test_get_first_found_item():
    sut = InventoryHandler(rows=5, columns=12)
    sut.set(cell_number=13, item="my value")
    sut.set(cell_number=12, item="my value")
    sut.set(cell_number=14, item="my value")
    expected = InventoryCell(cell_number=12, item="my value")

    assert sut.get_first_found_item("my value") == expected


def test_get_last_found_item():
    sut = InventoryHandler(rows=5, columns=12)
    sut.set(cell_number=12, item="my value")
    sut.set(cell_number=14, item="my value")
    sut.set(cell_number=13, item="my value")
    expected = InventoryCell(cell_number=14, item="my value")

    assert sut.get_last_found_item("my value") == expected


def test_cell_number_out_of_range_while_setting():
    with raises(CellNumberOutOfRange):
        sut = InventoryHandler(rows=2, columns=5)

        sut.set(cell_number=50, item="value")


def test_cell_number_out_of_range_while_getting():
    with raises(CellNumberOutOfRange):
        sut = InventoryHandler(rows=2, columns=5)

        sut.get(cell_number=50)


def test_set_item_into_first_found_empty_cell():
    sut = InventoryHandler(rows=5, columns=12, default_factory=lambda: "default")

    for i in range(1, 11):
        sut.set(cell_number=i, item="not empty")
    sut.set_into_first_found_empty_cell(item="my value")

    assert sut.get_first_found_item(item="my value") == InventoryCell(cell_number=11, item="my value")
