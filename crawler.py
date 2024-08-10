import aiohttp
import asyncio
from time import time
from aiohttp.client import ClientSession


class crawler:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_pages(self, session: ClientSession, page: int):
        async with session.get(f'{self.api_url}?pageIndex={page}', headers=self.headers) as response:
            try:
                data = await response.json()
                if data.get('status') and 'data' in data and 'ads' in data['data']:
                    return [self.extract_info(ad) for ad in data['data']['ads']]
                else:
                    print(f"Data not found on page {page}.")
            except aiohttp.ContentTypeError:
                print(f"Error parsing JSON on page {page}. Response content:", await response.text())

            except aiohttp.ClientResponseError as e:
                print(f"HTTP request error on page {page}: {e}")

    def extract_info(self, ad):
        details = ad.get('detail', {})
        price_info = ad.get('price', {})
        ad_info = {
            'title': details.get('title', 'نامشخص'),
            'color': details.get('color', 'نامشخص'),
            'mileage': details.get('mileage', 'نامشخص'),
            'location': details.get('location', 'نامشخص'),
            'code': details.get('code', 'نامشخص'),
            'url': details.get('url', 'نامشخص'),
            'image': details.get('image', 'نامشخص'),
            'time': details.get('time', 'نامشخص'),
            'price': price_info.get('price', 'نامشخص')
        }
        return ad_info
