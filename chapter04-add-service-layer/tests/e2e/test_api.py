import pytest
import requests


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock, random_uuid, config):
    sku, othersku = random_uuid(), random_uuid()
    early_batch = random_uuid()
    later_batch = random_uuid()
    other_batch = random_uuid()

    add_stock([
        (later_batch, sku, 100, "2011-01-02"),
        (early_batch, sku, 100, "2011-01-01"),
        (other_batch, sku, 100, None),
    ])
    data = {
        "order_id": random_uuid(), "sku": sku, "qty": 3
    }
    url = config.get_api_url()
    response = requests.post(url=f"{url}/allocate", json=data)

    assert response.status_code == 201
    assert response.json()["batch_ref"] == early_batch

