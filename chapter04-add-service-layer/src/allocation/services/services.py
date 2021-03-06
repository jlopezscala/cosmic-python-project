from datetime import date
from typing import Optional

from src.allocation.adapters.repository import AbstractRepository
from src.allocation.domain import model
from src.allocation.domain.model import OrderLine


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


class InvalidSku(Exception):
    pass


def allocate(line: OrderLine, batches, session) -> str:
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batch_ref = model.allocate(line, batches)
    session.commit()
    return batch_ref


def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        repo: AbstractRepository, session,
) -> None:
    repo.add(model.Batch(ref, sku, eta, qty))
    session.commit()
