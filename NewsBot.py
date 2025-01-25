import asyncio
import telebot.async_telebot
from newsdataapi import NewsDataApiClient
import re


class NewsBot(telebot.async_telebot.AsyncTeleBot):

    def __init__(self, token):
        super().__init__(token)
        self.newsapi = NewsDataApiClient(
            apikey="pub_53530a5051470fbecdfa3067a3f2b8bea6829"
        )
        self.list_of_data = {}
        self.list_of_categories = {
            "Горячие": "top",
            "Бизнес": "business",
            "Развлечения": "entertainment",
            "Здоровье": "health",
            "Мировые новости": "world",
            "Политика": "politics",
            "Наука": "science",
            "Спорт": "sports",
            "Технологии": "technology",
            "Еда": "food",
            "Все категории": None,
        }

    def escape_md(self, text: str):
        if text:
            escape_chars = r"_*[]()~`>#+-=|{}.!"
            return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)
        return text

    def escape_md_text_link(self, text: str):
        if text:
            escape_chars = r"\)"
            return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)
        return text

    async def start_command(
        self, message: telebot.async_telebot.types.Message
    ):
        self.list_of_data[message.chat.id] = {
            "top_headlines": {},
            "all_articles": {},
            "count": 0,
            "flag_for_q": False,
            "flag_for_source": False,
            "category": None,
            "q": None,
            "sources": None,
        }
        markup = telebot.async_telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        button = telebot.async_telebot.types.KeyboardButton("/set_sources")
        button2 = telebot.async_telebot.types.KeyboardButton("/set_category")
        button3 = telebot.async_telebot.types.KeyboardButton("/set_keyword")
        button4 = telebot.async_telebot.types.KeyboardButton("/get_filters")
        button5 = telebot.async_telebot.types.KeyboardButton("/get_news")
        markup.add(button, button2, button3, button4, button5)
        await self.send_message(
            message.chat.id,
            f"Привет {message.chat.first_name}! Я бот, который будет отправлять тебе новости по любой теме из главных новостей мира и твоей страны.",
            reply_markup=markup,
        )
        await self.send_message(
            message.chat.id,
            """Вы можете установить фильтры новостей по этим критериям:
1. /set_sources Источники (по умолчанию: Все источники)
2. /set_category Категория  (по умолчанию: Все категории)
3. /set_keyword Ключевое слово (по умолчанию: Без ключевого слова)""",
        )
        await self.send_message(
            message.chat.id,
            "Чтобы узнать настройки фильтров, выберите команду /get_filters, чтобы получить новости, выберите команду /get_news",
        )

    async def check_news(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["more_news"] = False
        markup = telebot.async_telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        button = telebot.async_telebot.types.KeyboardButton("/set_sources")
        button2 = telebot.async_telebot.types.KeyboardButton("/set_category")
        button3 = telebot.async_telebot.types.KeyboardButton("/set_keyword")
        button4 = telebot.async_telebot.types.KeyboardButton("/get_filters")
        button5 = telebot.async_telebot.types.KeyboardButton("/get_news")
        markup.add(button, button2, button3, button4, button5)
        await self.send_message(
            message.chat.id,
            f"""Запрос задан по следующим параметрам:
1. Источник: {self.list_of_data[message.chat.id]["sources"] if self.list_of_data[message.chat.id]["sources"] is not None else "Все источники"}
2. Категория: {next((key for key, value in self.list_of_categories.items() if value == self.list_of_data[message.chat.id]["category"]))}
3. Ключевое слово: {self.list_of_data[message.chat.id]["q"] if self.list_of_data[message.chat.id]["q"] is not None else "Без ключевого слова"}""",
        )

    async def get_news(self, message: telebot.types.Message):
        markup = telebot.async_telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        button = telebot.async_telebot.types.KeyboardButton("/set_sources")
        button2 = telebot.async_telebot.types.KeyboardButton("/set_category")
        button3 = telebot.async_telebot.types.KeyboardButton("/set_keyword")
        button4 = telebot.async_telebot.types.KeyboardButton("/get_filters")
        button5 = telebot.async_telebot.types.KeyboardButton("/get_news")
        markup.add(button, button2, button3, button4, button5)
        try:
            self.list_of_data[message.chat.id]["top_headlines"] = (
                self.newsapi.latest_api(
                    language="ru",
                    category=self.list_of_data[message.chat.id]["category"],
                    q=self.list_of_data[message.chat.id]["q"],
                    domain=self.list_of_data[message.chat.id]["sources"],
                    image=True,
                )
            )
            for i in range(
                len(
                    self.list_of_data[message.chat.id]["top_headlines"][
                        "results"
                    ]
                )
            ):
                data = self.list_of_data[message.chat.id]["top_headlines"][
                    "results"
                ][i]
                title = self.escape_md(data["title"])
                url = self.escape_md_text_link(data["link"])
                await self.send_photo(
                    message.chat.id,
                    self.list_of_data[message.chat.id]["top_headlines"][
                        "results"
                    ][i]["image_url"],
                    f"[{title}]({url})",
                    parse_mode="MarkdownV2",
                    reply_markup=markup,
                )
            if (
                len(
                    self.list_of_data[message.chat.id]["top_headlines"][
                        "results"
                    ]
                )
                == 0
            ):
                await self.send_message(
                    message.chat.id,
                    "По вашему запросу ничего не найдено. Попробуйте другой запрос, или подождите некоторое время, когда новости по вашим параметрам появятся",
                    reply_markup=markup,
                )
        except Exception:
            await self.send_message(
                message.chat.id,
                f"Произошла ошибка: скорее всего, вы неправильно указали название источника или этот источник не существует в нашей базе данных, попробуйте еще раз",
                reply_markup=markup,
            )

    async def set_sources(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["flag_for_source"] = True
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Все источники")
        markup.add(button)
        await self.send_message(
            message.chat.id,
            "Введите название источника латинскими буквами(как указано в домене сайта источника). Пример: rbc(РБК), bbc, lenta и так далее. Вы можете ввести до 5 источников, просто введите их через запятую. Если вы не хотите устанавливать никакие источники, то нажмите на кнопку ниже.",
            reply_markup=markup,
        )

    async def set_sources2(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["flag_for_source"] = False
        if message.text == "Все источники":
            self.list_of_data[message.chat.id]["sources"] = None
        elif message.text != "Все источники":
            self.list_of_data[message.chat.id]["sources"] = message.text.lower()  # type: ignore
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.async_telebot.types.KeyboardButton("/set_sources")
        button2 = telebot.async_telebot.types.KeyboardButton("/set_category")
        button3 = telebot.async_telebot.types.KeyboardButton("/set_keyword")
        button4 = telebot.async_telebot.types.KeyboardButton("/get_filters")
        button5 = telebot.async_telebot.types.KeyboardButton("/get_news")
        markup.add(button, button2, button3, button4, button5)
        await self.send_message(
            message.chat.id,
            "Источник задан.",
            reply_markup=markup,
        )

    async def set_category(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Горячие")
        button2 = telebot.types.KeyboardButton("Бизнес")
        button3 = telebot.types.KeyboardButton("Наука")
        button4 = telebot.types.KeyboardButton("Технологии")
        button5 = telebot.types.KeyboardButton("Здоровье")
        button6 = telebot.types.KeyboardButton("Спорт")
        button7 = telebot.types.KeyboardButton("Развлечения")
        button8 = telebot.types.KeyboardButton("Еда")
        button9 = telebot.types.KeyboardButton("Политика")
        button10 = telebot.types.KeyboardButton("Мировые новости")
        button11 = telebot.types.KeyboardButton("Все категории")
        markup.add(
            button,
            button2,
            button3,
            button4,
            button5,
            button6,
            button7,
            button8,
            button9,
            button10,
            button11,
        )
        await self.send_message(
            message.chat.id, "Выберите категорию", reply_markup=markup
        )

    async def set_category2(self, message: telebot.types.Message):
        if message.text in self.list_of_categories:
            self.list_of_data[message.chat.id]["category"] = (
                self.list_of_categories[message.text]
            )
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = telebot.async_telebot.types.KeyboardButton("/set_sources")
            button2 = telebot.async_telebot.types.KeyboardButton(
                "/set_category"
            )
            button3 = telebot.async_telebot.types.KeyboardButton(
                "/set_keyword"
            )
            button4 = telebot.async_telebot.types.KeyboardButton(
                "/get_filters"
            )
            button5 = telebot.async_telebot.types.KeyboardButton("/get_news")
            markup.add(button, button2, button3, button4, button5)
            await self.send_message(
                message.chat.id,
                "Категория задана",
                reply_markup=markup,
            )

    async def set_q(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["flag_for_q"] = True
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Без ключевого слова")
        markup.add(button)
        await self.send_message(
            message.chat.id, "Введите ключевое слово", reply_markup=markup
        )

    async def set_q2(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["flag_for_q"] = False
        if message.text == "Без ключевого слова":
            self.list_of_data[message.chat.id]["q"] = None
        elif message.text != "Без ключевого слова":
            self.list_of_data[message.chat.id]["q"] = message.text

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.async_telebot.types.KeyboardButton("/set_sources")
        button2 = telebot.async_telebot.types.KeyboardButton("/set_category")
        button3 = telebot.async_telebot.types.KeyboardButton("/set_keyword")
        button4 = telebot.async_telebot.types.KeyboardButton("/get_filters")
        button5 = telebot.async_telebot.types.KeyboardButton("/get_news")
        markup.add(button, button2, button3, button4, button5)
        await self.send_message(
            message.chat.id,
            "Ключевое слово задано",
            reply_markup=markup,
        )

    async def run(self):
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(
            self.check_news, commands=["get_filters"]
        )
        self.register_message_handler(self.get_news, commands=["get_news"])
        self.register_message_handler(
            self.set_sources, commands=["set_sources"]
        )
        self.register_message_handler(
            self.set_sources2,
            func=lambda message: True
            and self.list_of_data[message.chat.id]["flag_for_source"] is True,
        )
        self.register_message_handler(
            self.set_category, commands=["set_category"]
        )
        self.register_message_handler(
            self.set_category2,
            func=lambda message: message.text in self.list_of_categories,
        )
        self.register_message_handler(self.set_q, commands=["set_keyword"])
        self.register_message_handler(
            self.set_q2,
            func=lambda message: True
            and self.list_of_data[message.chat.id]["flag_for_q"] is True,
        )

        await self.polling(none_stop=True, interval=0)
