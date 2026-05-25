import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiTelegramException
from newsdataapi import NewsDataApiClient
import re


class NewsBotForChannel_ru(AsyncTeleBot):

    def __init__(self, token):
        super().__init__(token)
        self.newsapi = NewsDataApiClient(
            apikey="pub_53530a5051470fbecdfa3067a3f2b8bea6829"
        )
        self.list_of_used_news = []
        self.flag = True
        self.flag2 = True

    def escape_md(self, text: str):
        if text:
            escape_chars = r"_*[]()~`>#+-=|{}.!"
            return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    def escape_md_text_link(self, text: str):
        if text:
            escape_chars = r"\)"
            return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    async def send_news(self, Chat_id):
        while True:
            top_headlines = self.newsapi.latest_api(
                country="ru",
                image=True,
                language="ru",
                excludedomain="english.pravda.ru, russian.rt.com, aif.ru, iz.ru, eadaily.com",
            )

            for i in range(len(top_headlines["results"])):
                if (
                    top_headlines["results"][i]["link"]
                    not in self.list_of_used_news
                ):
                    data = top_headlines["results"][i]
                    title = self.escape_md(data["title"])
                    url = self.escape_md_text_link(data["link"])
                    try:
                        await self.send_photo(
                            Chat_id,
                            top_headlines["results"][i]["image_url"],
                            f"[{title}]({url})",
                            parse_mode="MarkdownV2",
                        )
                    except ApiTelegramException:
                        await self.send_message(
                            Chat_id,
                            f"[{title}]({url})",
                            parse_mode="MarkdownV2",
                        )
                    print(top_headlines["results"][i]["source_name"])
                    self.list_of_used_news.append(
                        top_headlines["results"][i]["link"]
                    )

            await asyncio.sleep(3600)

    async def Clear_list(self):
        while True:
            await asyncio.sleep(86400)
            del self.list_of_used_news[0 : len(self.list_of_used_news) - 20]

    async def run(self):
        task1 = asyncio.create_task(self.Clear_list())
        task2 = asyncio.create_task(self.send_news(-1002748974907))
        await asyncio.gather(task1, task2)
        await self.polling(none_stop=True, interval=0)
