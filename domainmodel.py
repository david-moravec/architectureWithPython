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
        return hash(self.id)

    def same_SKU(self, o: "OrderLine") -> bool:
        return self.sku == o.sku


class Batch:
    def __init__(
        self, reference: int, sku: str, purchased_quantity: int, eta: Optional[date]
    ) -> None:
        self.reference = reference
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = purchased_quantity
        self._allocations: set[OrderLine] = set()

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def allocate(self, order: OrderLine) -> None:
        if not self._is_allocated(order):
            self._allocations.add(order)

    def deallocate(self, order: OrderLine) -> bool:
        if self._is_allocated(order):
            self._allocations.remove(order)

    def can_allocate(self, order: OrderLine) -> bool:
        if self._compatible_sku(order):
            return self.available_quantity >= order.quantity

        return False

    def _compatible_sku(self, order: OrderLine) -> bool:
        return self.sku == order.sku

    def _is_allocated(self, order: OrderLine) -> bool:
        return order in self._allocations
