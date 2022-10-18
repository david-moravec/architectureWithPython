from ast import Raise
from dataclasses import dataclass


from enum import Enum

@dataclass(frozen=True, kw_only=True)
class Order:
    sku: str = None
    quantity: int = 0

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("Cannot have negative quantity")

    def __eq__(self, o: "Order") -> bool:
        if self.same_SKU(o):
            return self.quantity == o.quantity

        return False
        
    def __sub__(self, o: "Order") -> "Order":
        if not self.same_SKU(o):
            raise ValueError('Incompatible SKU')

        difference: int = self.quantity - o.quantity
        
        return Order(sku=self.sku, quantity=difference)

    def __str__(self) -> str:
        return f'SKU = {self.sku}, quantity = {self.quantity}'
        

    def same_SKU(self, o: "Order") -> bool:
        return self.sku == o.sku


class Batch:
    def __init__(self, reference: int, contents: Order) -> None:
        self.reference = reference
        self.contents = contents
        self._past_orders: set[Order] = set()

    def allocate_order(self, order: Order) -> bool:
        if order in self._past_orders:
            return False

        self.contents = self.contents - order

        self._past_orders.add(Order)

        return True