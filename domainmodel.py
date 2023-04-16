from typing import Optional
from datetime import date

from dataclasses import dataclass


class SkuErorr(Exception):
    pass


@dataclass(frozen=True, kw_only=True)
class Order:
    sku: str
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("Cannot have negative quantity")

    def __eq__(self, o: "Order") -> bool:
        if self.same_SKU(o):
            return self.quantity == o.quantity

        return False

    def __sub__(self, o: "Order") -> "Order":
        if not self.same_SKU(o):
            raise ValueError("Incompatible SKU")

        difference: int = self.quantity - o.quantity

        return Order(sku=self.sku, quantity=difference)

    def __str__(self) -> str:
        return f"SKU = {self.sku}, quantity = {self.quantity}"

    def __hash__(self) -> int:
        return self.orderid

    def same_SKU(self, o: "Order") -> bool:
        return self.sku == o.sku


class OrderLine(Order):
    orderid: int


class Batch:
    def __init__(self, reference: int, contents: Order, eta: Optional[date]) -> None:
        self.reference = reference
        self.available = contents
        self.eta = eta
        self._past_orders: set[Order] = set()

    def compatible_sku(self, order: Order) -> bool:
        return self.available.same_SKU(order)

    def add_available_quantity(self, to_add: Order) -> None:
        if not self.compatible_sku(to_add):
            return

        available = self.available

        self.available = Order(
            sku=available.sku, quantity=available.quantity + to_add.quantity
        )

    def allocate_order(self, order: Order) -> bool:
        if order in self._past_orders:
            return False

        self.available = self.available - order

        self._past_orders.add(Order)

        return True

    def can_allocate(self, order: Order) -> bool:
        if self.compatible_sku(order):
            return self.available.quantity >= order.quantity

        return False
