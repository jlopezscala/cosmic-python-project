from datetime import date, timedelta
import pytest

from app.model.my_model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    # Given
    batch = Batch(batch_id=1, eta=today, sku=22, available_quantity=12)

    # When
    batch.allocate(OrderLine(order_id=2, sku=22, quantity=2))

    # Then
    assert batch.available_quantity == 10


def test_can_allocate_if_available_greater_than_required():
    # Given
    batch = Batch(batch_id=1, eta=today, sku=22, available_quantity=12)
    existing_order_line = OrderLine(order_id=2, sku=22, quantity=2)
    batch.allocate(existing_order_line)

    # When
    batch.allocate(OrderLine(order_id=3, sku=22, quantity=2))

    # Then
    assert batch.available_quantity == 8


def test_cannot_allocate_if_available_smaller_than_required():
    # Given
    batch = Batch(batch_id=1, eta=today, sku=22, available_quantity=2)

    # When
    assert not batch.can_allocate(OrderLine(order_id=3, sku=22, quantity=3))


def test_can_allocate_if_available_equal_to_required():
    # Given
    batch = Batch(batch_id=1, eta=today, sku=22, available_quantity=3)

    # When
    assert batch.can_allocate(OrderLine(order_id=3, sku=22, quantity=3))



def test_cannot_allocate_different_skus():
    # Given
    batch = Batch(batch_id=1, eta=today, sku=20, available_quantity=2)

    # When
    assert not batch.can_allocate(OrderLine(order_id=3, sku=22, quantity=2))


def test_prefers_warehouse_batches_to_shipments():
    pass
    # # Given
    # warehouse_batch = Batch(id=1, eta=today, product_sku=22, quantity=5, status="warehouse")
    # shipping_batch = Batch(id=1, eta=today, product_sku=22, quantity=3, status="shipping")
    #
    # # When
    # allocation_service.allocate_order_line(OrderLine(id=3, product_sku=22, quantity=2))
    #
    # # Then
    # assert len(warehouse_batch.order_lines) == 1
    # assert len(shipping_batch.order_lines) == 0
    # assert warehouse_batch.quantity == 2
    # assert shipping_batch.quantity == 3


def test_prefers_earlier_batches():
    pass
    # Given
    # batch1 = Batch(id=1, eta=today, product_sku=22, quantity=5, status="warehouse")
    # later_batch = Batch(id=1, eta=later, product_sku=22, quantity=3, status="shipping")
    #
    # # When
    # allocation_service.allocate_order_line(OrderLine(id=3, product_sku=22, quantity=2))
    #
    # # Then
    # assert len(batch1.order_lines) == 1
    # assert len(later_batch.order_lines) == 0
    # assert batch1.quantity == 2
    # assert later_batch.quantity == 3
