import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch_html(session, url, params, headers):
    async with session.get(url, params=params, headers=headers, timeout=30) as response:
        return await response.text()

async def get_html(query):
    params = {
        "q": query,
        "hl": "ru",
        "gl": "ru",
        "start": 0,
        "num": 1
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    page_limit = 1
    page_num = 0

    data = []

    async with aiohttp.ClientSession() as session:
        while True:
            page_num += 1

            html = await fetch_html(session, "https://www.google.com/search", params, headers)
            soup = BeautifulSoup(html, 'lxml')

            for result in soup.select(".tF2Cxc"):
                title = result.select_one(".DKV0Md").text
                try:
                    snippet = result.select_one(".lEBKkf span").text
                except:
                    snippet = None
                links = result.select_one(".yuRUbf a")["href"]

                data.append({
                    "title": title,
                    "snippet": snippet,
                    "links": links
                })

            if page_num == page_limit:
                break
            if soup.select_one(".d6cvqb a[id=pnnext]"):
                params["start"] += 10
            else:
                break
    if data:
        return data[0]["links"]
    else:
        print(query)
        return None
