from test_database import db
from unittest.mock import patch, AsyncMock
import pytest
from aiohttp.client import ClientSession
from crawler import crawler


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
