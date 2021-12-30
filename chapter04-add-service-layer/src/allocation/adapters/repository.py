from abc import ABC, abstractmethod

from src.allocation.domain import model


class AbstractRepository(ABC):
    """
    A thought on ABCs:
    They look cool when trying to mimic what Interfaces are in Java.
    In real life, I would omit using ABCs for production code.
    Python makes it too easy to ignore them and ABCs end up being unmaintained or misleading.

    I would better rely on Python duck typing to enable abstractions.

    Alternative for Python >3.8 are Protocols: https://www.python.org/dev/peps/pep-0544

    """

    @abstractmethod  # Makes ABCs work in Python. Interpreter will refuse to instantiate a class
    # that does not implement all the abstract methods from the parent classes.
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError  # Nice but not sufficient nor necessary.


class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch: model.Batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
