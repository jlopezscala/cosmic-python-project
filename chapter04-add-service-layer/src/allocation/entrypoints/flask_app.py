from http import HTTPStatus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from ..adapters import orm, repository

from flask import Flask, request, jsonify

from ..domain import model
from ..services import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate():
    session = get_session()
    batches = repository.SQLAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json["order_id"],
        request.json["sku"],
        request.json["qty"],
    )
    try:
        batch_ref = services.allocate(line, batches)
    except (model.OutOfStockError, services.InvalidSku) as err:
        return jsonify({f"message": str(err)}), HTTPStatus.BAD_REQUEST

    return jsonify({"batch_ref": batch_ref}), HTTPStatus.CREATED
