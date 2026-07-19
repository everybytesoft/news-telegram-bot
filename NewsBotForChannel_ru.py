import asyncio
from telebot.async_telebot import AsyncTeleBot
from newsdataapi import NewsDataApiClient
import re


class NewsBotForChannel_ru(AsyncTeleBot):

    # Белый список доверенных источников (редакционный выбор — список
    # составлен пользователем проекта). Значения — не домены сайтов, а
    # внутренний "source_id" NewsData: параметр domain матчится именно по
    # нему, а не по доменному имени (найдено эмпирически).
    #
    # Category-фильтр сознательно не используется: разные издания
    # размечены разными категориями в базе NewsData (например, у Forbes
    # почти всё помечено "business", а не "top"), единый фильтр
    # несправедливо вырезал бы часть источников. Отбор по теме/важности
    # тут и так обеспечивает сам список доверенных изданий.
    #
    # themoscowtimes сейчас не даёт постов: в базе NewsData у этого
    # источника только англоязычные статьи. rosbalt_ru тоже сейчас пуст —
    # NewsData давно не индексировал оттуда ничего нового. Оба варианта —
    # ограничения самого NewsData, поправить нашей стороной нельзя;
    # оставлены в списке на случай, если ситуация изменится.
    #
    # ВАЖНО: тариф NewsData ограничивает параметр domain максимум 5
    # значениями за запрос (иначе UnsupportedQueryLength). Поэтому список
    # разбит на группы по 4 источника, и send_news при каждом запуске
    # (раз в час) берёт следующую группу по кругу — так за несколько
    # часов используются все источники, и не приходится никого вычёркивать.
    TRUSTED_DOMAINS = [
        "themoscowtimes",  # The Moscow Times
        "forbes_ru",  # Forbes
        "novayagazeta",  # Новая газета
        "euronews_ru",  # Euronews
        "lenta",  # Lenta
        "rbc",  # РБК
        "vedomosti",  # Ведомости
        "kommersant_ru",  # Коммерсантъ
        "interfax",  # Интерфакс
        "rosbalt_ru",  # Росбалт
        "gazeta_ru",  # Газета.ру
        "ng_ru",  # Независимая газета
    ]
    DOMAIN_GROUP_SIZE = 4

    # Внутри группы каждый домен запрашивается отдельным вызовом API и
    # берётся не больше этого числа свежих статей — иначе более активные
    # издания (например, Euronews) забивали бы собой всю выдачу и
    # заглушали редкопубликующиеся источники (так уже случилось один раз).
    ARTICLES_PER_DOMAIN = 2

    # Максимальная длина описания в посте (символов).
    MAX_DESCRIPTION_LENGTH = 400

    def __init__(self, token):
        super().__init__(token)
        self.newsapi = NewsDataApiClient(
            apikey="pub_53530a5051470fbecdfa3067a3f2b8bea6829"
        )
        self.list_of_used_news = []
        self.flag = True
        self.flag2 = True
        self.domain_groups = [
            self.TRUSTED_DOMAINS[i : i + self.DOMAIN_GROUP_SIZE]
            for i in range(
                0, len(self.TRUSTED_DOMAINS), self.DOMAIN_GROUP_SIZE
            )
        ]
        self.domain_group_index = 0

    def escape_md(self, text: str):
        if text:
            escape_chars = r"_*[]()~`>#+-=|{}.!"
            return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    def escape_md_text_link(self, text: str):
        if text:
            escape_chars = r"\)"
            return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    # Мусорный шаблон, который многие WordPress-агрегаторы добавляют в конец
    # описания при перепечатке чужих статей, например:
    # "The post <заголовок> first appeared on <сайт>."
    BOILERPLATE_RE = re.compile(
        r"\s*the post .* first appeared on .*\.?\s*$",
        re.IGNORECASE | re.DOTALL,
    )

    def shorten_description(self, text: str):
        if not text:
            return None
        text = self.BOILERPLATE_RE.sub("", text)
        text = " ".join(text.split())
        if not text:
            return None
        if len(text) <= self.MAX_DESCRIPTION_LENGTH:
            return text
        return text[: self.MAX_DESCRIPTION_LENGTH].rsplit(" ", 1)[0] + "…"

    def build_caption(self, data: dict):
        title = self.escape_md(data.get("title"))
        url = self.escape_md_text_link(data.get("link"))
        description = self.escape_md(
            self.shorten_description(data.get("description"))
        )
        source = self.escape_md(
            data.get("source_name") or data.get("source_id")
        )

        parts = [f"*[{title}]({url})*"]
        if description:
            parts.append(description)
        if source:
            parts.append(f"🔗 Источник: {source}")
        return "\n\n".join(parts)

    async def send_news(self, Chat_id):
        while True:
            current_group = self.domain_groups[self.domain_group_index]
            self.domain_group_index = (self.domain_group_index + 1) % len(
                self.domain_groups
            )

            for domain in current_group:
                try:
                    top_headlines = self.newsapi.latest_api(
                        image=True,
                        language="ru",
                        domain=domain,
                        size=self.ARTICLES_PER_DOMAIN,
                    )
                except Exception as e:
                    print(
                        f"[NewsBotForChannel_ru] Ошибка запроса к NewsData ({domain}): {e}"
                    )
                    continue

                for data in top_headlines.get("results", []):
                    if data["link"] in self.list_of_used_news:
                        continue

                    caption = self.build_caption(data)
                    image_url = data.get("image_url")
                    sent = False
                    if image_url:
                        try:
                            await self.send_photo(
                                Chat_id,
                                image_url,
                                caption,
                                parse_mode="MarkdownV2",
                            )
                            sent = True
                        except Exception:
                            sent = False
                    if not sent:
                        await self.send_message(
                            Chat_id,
                            caption,
                            parse_mode="MarkdownV2",
                        )
                    self.list_of_used_news.append(data["link"])

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
