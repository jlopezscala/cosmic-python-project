from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from ..adapters import orm, repository

from flask import Flask, request, jsonify

from ..domain import model

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

    batch_ref = model.allocate(line, batches)

    return jsonify({"batch_ref": batch_ref}), 201
