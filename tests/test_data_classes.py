from pytest import raises

from game_inventory import *


class SomeItemForTests(InventoryItem):
    @property
    def max_stack(self) -> int:
        return 10


def test_max_size_of_sextant_is_frozen():
    sut = SomeItemForTests(amount=7)

    with raises(AttributeError):
        sut.max_stack = 15


def test_amount_cant_be_greater_than_max_stack_in_init_in_item():
    with raises(ValueError):
        SomeItemForTests(100)


def test_amount_cant_be_greater_than_max_stack_in_item():
    sut = SomeItemForTests(amount=7)

    with raises(ValueError):
        sut.amount = 100


def test_amount_cant_be_lower_zero_in_init_in_item():
    with raises(ValueError):
        SomeItemForTests(-1)


def test_amount_cant_be_lower_zero_in_item():
    sut = SomeItemForTests(amount=7)

    with raises(ValueError):
        sut.amount = -1
