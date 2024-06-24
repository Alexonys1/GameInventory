class ItemNotFound(Exception):
    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return f"{self.item} has not found in inventory!"


class CellNumberOutOfRange(Exception):
    def __init__(self, cell_number: int, max_cell_number: int):
        self.cell_number = cell_number
        self.max_cell_number = max_cell_number

    def __repr__(self):
        return (
            f"cell_number must belong between 1 and {self.max_cell_number}"
            f"not {self.cell_number}!"
        )
