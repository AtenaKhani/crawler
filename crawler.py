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



                

