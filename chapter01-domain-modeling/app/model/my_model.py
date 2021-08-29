from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:

    def __init__(self, batch_id: str, sku: str, eta: datetime, available_quantity: int):
        self._batch_id = batch_id,
        self.sku = sku
        self.eta = eta
        self.available_quantity = available_quantity

    def allocate(self, order_line: OrderLine):
        self.available_quantity -= order_line.quantity

    def can_allocate(self, order_line: OrderLine):
        return order_line.sku == self.sku and order_line.quantity <= self.available_quantity
