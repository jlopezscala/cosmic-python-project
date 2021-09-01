from dataclasses import dataclass
from datetime import datetime
from typing import Set


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:

    def __init__(self, batch_id: str, sku: str, eta: datetime, quantity: int):
        self._batch_id = batch_id,
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations: Set[OrderLine] = set()

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def allocate(self, order_line: OrderLine):
        if self.can_allocate():
            self._allocations.add(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return order_line.sku == self.sku and order_line.quantity <= self.available_quantity

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self._allocations.remove(order_line)
