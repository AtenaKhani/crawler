from test_database import db
from unittest.mock import patch, AsyncMock
import pytest
from aiohttp.client import ClientSession
from crawler import crawler
from models import Car


@pytest.fixture
def fetcher(db):
    return crawler('https://bama.ir/cad/api/search', db)


@pytest.mark.asyncio
@patch('aiohttp.ClientSession.get')
async def test_fetch_pages(mock_get, fetcher):
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "status": True,
        "data": {
            "ads": [
                {
                    "detail": {
                        "title": "test",
                        "color": "red",
                        "mileage": "10000",
                        "location": "city",
                        "code": "12345",
                        "url": "http://example.com",
                        "image": "http://imageurl.com",
                        "time": "2024-01-10",
                    },
                    "price": {
                        "price": "300000"
                    }
                }
            ]
        }
    }
    mock_get.return_value.__aenter__.return_value = mock_response

    async with ClientSession() as session:
        data = await fetcher.fetch_pages(session, 1)
        assert len(data) == 1
        assert data[0].title == "test"
        assert data[0].price == "300000"


def test_extract_info(fetcher):
    ad = {
        'detail': {
            'title': 'test',
            'color': 'red',
            'mileage': '1000',
            'location': 'city',
            'code': '12345',
            'url': 'http://example.com',
            'image': 'http://imageurl.com',
            'time': '2024-01-10',
        },
        'price': {
            'price': '5000'
        }
    }
    car = fetcher.extract_info(ad)

    assert car.title == 'test'
    assert car.color == 'red'
    assert car.mileage == '1000'
    assert car.location == 'city'
    assert car.code == '12345'
    assert car.url == 'http://example.com'
    assert car.image == 'http://imageurl.com'
    assert car.time == '2024-01-10'
    assert car.price == '5000'


@pytest.mark.asyncio
async def test_create_and_run_tasks(db, fetcher):
    # Mock the fetch_pages method to return a list of Car objects
    fetcher.fetch_pages = AsyncMock(return_value=[
        Car(
            title="test", color="blue", mileage="20000", location="city",
            code="12345", url="http://example.com", image="http://imageurl.com",
            time="2024-01-10", price="40000"
        )
    ])

    # run the create_and_run_tasks method
    await fetcher.create_and_run_tasks(1)

    # verify that the fetch_pages method was called exactly once
    fetcher.fetch_pages.assert_called_once()

    # verify that the data was saved correctly in database
    with db.Session() as session:
        result = session.query(Car).filter_by(title="test").first()
        assert result is not None
        assert result.color == "blue"
        assert result.price == "40000"
