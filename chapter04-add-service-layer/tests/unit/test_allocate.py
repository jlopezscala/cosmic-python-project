from datetime import date, timedelta

from src.allocation.domain.model import Batch, OrderLine, allocate, OutOfStockError
import pytest

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    # Given
    in_stock_batch = Batch("in-stock-batch", sku="RETRO_CLOCK", quantity=100, eta=None)
    shipment_batch = Batch("shipment-batch", sku="RETRO_CLOCK", quantity=100, eta=None)
    line = OrderLine("oref", "RETRO_CLOCK", 10)

    # When
    allocate(line, [in_stock_batch, shipment_batch])

    # Then
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    # Given
    earliest = Batch("in-stock-batch", sku="RETRO_CLOCK", quantity=100, eta=None)
    medium = Batch("shipment-batch", sku="RETRO_CLOCK", quantity=100, eta=None)
    latest = Batch("shipment-batch", sku="RETRO_CLOCK", quantity=100, eta=None)
    line = OrderLine("oref", "RETRO_CLOCK", 10)

    # When
    allocate(line, [earliest, medium, latest])

    # Then
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    # Given
    in_stock = Batch("in-stock-batch", sku="RETRO_CLOCK", quantity=100, eta=None)
    shipment_batch = Batch("shipment-batch", sku="RETRO_CLOCK", quantity=100, eta=None)
    line = OrderLine("oref", "RETRO_CLOCK", 10)

    # When
    allocation = allocate(line, [in_stock, shipment_batch])

    # Then
    assert allocation == in_stock.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    # Given
    batch = Batch("batch1", sku="SMALL_FORK", quantity=10, eta=None)
    allocate(line=OrderLine("order1", "SMALL_FORK", 10), batches=[batch])

    # When
    with pytest.raises(OutOfStockError, match="SMALL_FORK"):
        allocate(line=OrderLine("order1", "SMALL_FORK", 1), batches=[batch])
