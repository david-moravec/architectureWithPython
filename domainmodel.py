from typing import Optional
from datetime import date

from dataclasses import dataclass


class SkuErorr(Exception):
    pass


@dataclass(frozen=True, kw_only=True)
class OrderLine:
    id: str
    sku: str
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("Cannot have negative quantity")

    def __eq__(self, o: "OrderLine") -> bool:
        if self.same_SKU(o):
            return self.quantity == o.quantity

        return False

    def __str__(self) -> str:
        return f"SKU = {self.sku}, quantity = {self.quantity}"

    def __hash__(self) -> int:
        return self.orderid

    def same_SKU(self, o: "OrderLine") -> bool:
        return self.sku == o.sku


class Batch:
    def __init__(
        self, reference: int, sku: str, quantity: int, eta: Optional[date]
    ) -> None:
        self.reference = reference
        self.available = quantity
        self.sku = sku
        self.eta = eta
        self._past_orders: set[OrderLine] = set()

    def compatible_sku(self, order: OrderLine) -> bool:
        return self.sku == order.sku

    def add_available_quantity(self, to_add: OrderLine) -> None:
        if not self.compatible_sku(to_add):
            return

        self.available = self.available + to_add.quantity

    def allocate_order(self, order: OrderLine) -> bool:
        if order in self._past_orders:
            return False

        self.available = self.available - order.quantity

        self._past_orders.add(OrderLine)

        return True

    def can_allocate(self, order: OrderLine) -> bool:
        if self.compatible_sku(order):
            return self.available >= order.quantity

        return False
