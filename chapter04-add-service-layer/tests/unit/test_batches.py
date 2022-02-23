from datetime import date, timedelta

from src.allocation.domain.model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    # Given
    batch = Batch(reference="ref", eta=today, sku="22", quantity=12)

    # When
    batch.allocate(OrderLine(order_id="2", sku="22", quantity=2))

    # Then
    assert batch.available_quantity == 10


def test_can_allocate_if_available_greater_than_required():
    # Given
    batch = Batch(reference="ref", eta=today, sku="22", quantity=12)
    existing_order_line = OrderLine(order_id="2", sku="22", quantity=2)
    batch.allocate(existing_order_line)

    # When
    batch.allocate(OrderLine(order_id="3", sku="22", quantity=2))

    # Then
    assert batch.available_quantity == 8


def test_cannot_allocate_if_available_smaller_than_required():
    # Given
    batch = Batch(reference="ref", eta=today, sku="22", quantity=2)

    # When
    assert not batch.can_allocate(OrderLine(order_id="3", sku="22", quantity=3))


def test_can_allocate_if_available_equal_to_required():
    # Given
    batch = Batch(reference="ref", eta=today, sku="22", quantity=3)

    # When
    assert batch.can_allocate(OrderLine(order_id="3", sku="22", quantity=3))


def test_cannot_allocate_different_skus():
    # Given
    batch = Batch(reference="ref", eta=today, sku="20", quantity=2)

    # When
    assert not batch.can_allocate(OrderLine(order_id="3", sku="22", quantity=2))


def test_can_only_deallocate_existing_lines():
    batch = Batch(reference="ref", eta=today, sku="20", quantity=6)
    unallocated_line = OrderLine(order_id="1", quantity=2, sku="20")
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 6
