import pytest
from models import Database, Car


@pytest.fixture
def db():
    database = Database('sqlite:///:memory:')
    return database


def test_save_data(db):
    car = Car(
        title="test", color="red", mileage="10000", location="city",
        code="12345", url="http://example.com", image="http://imageurl.com",
        time="2024-01-10", price="300000"
    )
    db.save_data([car])
    with db.Session() as session:
        result = session.query(Car).filter_by(title="test").first()
        assert result is not None
        assert result.color == "red"
        assert result.price == "300000"
