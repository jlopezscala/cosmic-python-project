from http import HTTPStatus

import pytest
import requests

from src.allocation import config


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock, random_uuid, config):
    sku, other_sku = random_uuid(), random_uuid()
    early_batch = random_uuid()
    later_batch = random_uuid()
    other_batch = random_uuid()

    add_stock([
        (later_batch, sku, 100, "2011-01-02"),
        (early_batch, sku, 100, "2011-01-01"),
        (other_batch, other_sku, 100, None),
    ])
    data = {
        "order_id": random_uuid(), "sku": sku, "qty": 3
    }
    url = config.get_api_url()
    response = requests.post(url=f"{url}/allocate", json=data)

    assert response.status_code == 201
    assert response.json()["batch_ref"] == early_batch


@pytest.mark.usefixtures("restart_api")
def test_allocations_are_persisted(add_stock, random_uuid):
    sku = random_uuid()
    batch1, batch2 = random_uuid(), random_uuid()
    order1, order2 = random_uuid(), random_uuid()

    add_stock([
        (batch1, sku, 10, "2011-01-01"),
        (batch2, sku, 10, "2011-01-02")
    ])

    line1 = {"order_id": order1, "sku": sku, "qty": 10}
    line2 = {"order_id": order2, "sku": sku, "qty": 10}
    url = config.get_api_url()

    r = requests.post(f"{url}/allocate", json=line1)
    assert r.status_code == HTTPStatus.CREATED
    assert r.json()["batch_ref"] == batch1

    r = requests.post(f"{url}/allocate", json=line2)
    assert r.status_code == HTTPStatus.CREATED
    assert r.json()["batch_ref"] == batch2
