from datetime import datetime
from http import HTTPStatus
import logging

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
    logging.info(config.get_postgres_uri())
    session = get_session()
    batches = repository.SQLAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json["order_id"],
        request.json["sku"],
        request.json["qty"],
    )
    try:
        batch_ref = services.allocate(line, batches, session)
    except (model.OutOfStockError, services.InvalidSku) as err:
        return jsonify({f"message": str(err)}), HTTPStatus.BAD_REQUEST

    return jsonify({"batch_ref": batch_ref}), HTTPStatus.CREATED


@app.route("/add_batch", methods=["POST"])
def add_batch():
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json["ref"],
        request.json["sku"],
        request.json["qty"],
        eta,
        repo,
        session,
    )
    return "OK", 201
