import aiohttp
import asyncio
from time import time
from aiohttp.client import ClientSession
from models import Car, Database


class crawler:
    def __init__(self, api_url: str, db: Database):
        self.api_url = api_url
        self.db = db
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def fetch_pages(self, session: ClientSession, page: int):
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
        if details is None:
            details = {}
        if price_info is None:
            price_info = {}
        return Car(
            title=details.get('title', 'نامشخص'),
            color=details.get('color', 'نامشخص'),
            mileage=details.get('mileage', 'نامشخص'),
            location=details.get('location', 'نامشخص'),
            code=details.get('code', 'نامشخص'),
            url=details.get('url', 'نامشخص'),
            image=details.get('image', 'نامشخص'),
            time=details.get('time', 'نامشخص'),
            price=price_info.get('price', 'نامشخص')
        )

    async def create_and_run_tasks(self, pages: int):
        all_data = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_pages(session, page) for page in range(1, pages + 1)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, list):
                    all_data.extend(result)
        self.db.save_data(all_data)
        print(f"{len(all_data)} ads have been successfully extracted and stored in the database.")


if __name__ == "__main__":
    db = Database('sqlite:///car.db')
    fetcher = crawler('https://bama.ir/cad/api/search', db)
    print("Crawling process started...")
    start = time()
    asyncio.run(fetcher.create_and_run_tasks(950))
    print(f"run time: {time() - start} seconds")
