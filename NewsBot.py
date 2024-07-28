import telebot
from newsapi import NewsApiClient


class NewsBot(telebot.TeleBot):

    def __init__(self, token):
        super().__init__(token)
        self.newsapi = NewsApiClient(
            api_key='24e1e7ae37b7406f9d529f9859172fa4')
        self.list_of_data = {}
        self.list_of_sorces = {
            "Google News (Russia)": 'google-news-ru',
            "Лента.ру": 'lenta',
            "РБК": 'rbc',
            "RT": 'rt',
            "Все источники": None
        }
        self.list_of_categorys = {
            "Бизнес": 'business',
            "Развлечения": 'entertainment',
            "Общие": 'general',
            "Здоровье": 'health',
            "Наука": 'science',
            "Спорт": 'sports',
            "Технологии": 'technology',
            "Все категории": None
        }

    def buttons(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.list_of_data[message.chat.id]["sources"] is not None:
            button = telebot.types.KeyboardButton("Задать источник")
            button2 = telebot.types.KeyboardButton("Задать ключевое слово")
            markup.add(button, button2)
        elif self.list_of_data[message.chat.id]["category"] is not None:
            button = telebot.types.KeyboardButton("Задать категорию")
            button2 = telebot.types.KeyboardButton("Задать ключевое слово")
            markup.add(button, button2)
        else:
            button = telebot.types.KeyboardButton("Задать источник")
            button2 = telebot.types.KeyboardButton("Задать категорию")
            button3 = telebot.types.KeyboardButton("Задать ключевое слово")
            markup.add(button, button2, button3)
        return markup

    def buttons2(self):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Задать источник")
        button2 = telebot.types.KeyboardButton("Задать ключевое слово")
        markup.add(button, button2)
        return markup

    def start_command(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id] = {
            "top_headlines": {},
            "all_articles": {},
            "count": 0,
            "more_news": False,
            "flag_for_q": False,
            "category": None,
            "q": None,
            "sources": None,
            "sources_more_news": None,
            "q_more_news": None
        }
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Задать источник")
        button2 = telebot.types.KeyboardButton("Задать категорию")
        button3 = telebot.types.KeyboardButton("Задать ключевое слово")
        button4 = telebot.types.KeyboardButton("/news")
        markup.add(button, button2, button3, button4)
        self.send_message(
            message.chat.id,
            "Привет! Я бот, который будет отправлять тебе новости по любой теме из главных новостей мира и твоей страны.",
            reply_markup=markup)
        self.send_message(
            message.chat.id, """Вы можете задать:
1. Источники: По умолчанию все источники.
2. Категорию новостей: По умолчанию все категории.
3. Ключевое слово: любое слово на вашем языке. По умолчанию без ключевого слова."""
        )
        self.send_message(
            message.chat.id,
            "Параметр источников нельзя указывать вместе категорией. Либо источник, либо категория."
        )
        self.send_message(
            message.chat.id,
            "Чтобы узнать найстроки параметров и получить новости, выбирете команду /news"
        )

    def get_news(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["more_news"] = False
        markup = self.buttons(message)
        buttonsp = telebot.types.KeyboardButton("Получить новости")
        markup.add(buttonsp)
        self.send_message(
            message.chat.id, f"""Запрос задан по следующим параметрам:
1. Источник: {next((key for key, value in self.list_of_sorces.items() if value == self.list_of_data[message.chat.id]["sources"]))}
2. Категория: {next((key for key, value in self.list_of_categorys.items() if value == self.list_of_data[message.chat.id]["category"]))}
3. Ключевое слово: {self.list_of_data[message.chat.id]["q"] if self.list_of_data[message.chat.id]["q"] is not None else "Без ключевого слова"}"""
        )
        self.send_message(
            message.chat.id,
            "Если вы хотите изменить параметры запроса, нажмите на кнопки ниже, иначе нажмите на кнопку 'Получить новости'",
            reply_markup=markup)

    def get_news2(self, message: telebot.types.Message):
        markup = self.buttons(message)
        buttonsp = telebot.types.KeyboardButton("/news")
        buttonsp2 = telebot.types.KeyboardButton("/more_news")
        markup.add(buttonsp, buttonsp2)
        self.list_of_data[
            message.chat.id]['top_headlines'] = self.newsapi.get_top_headlines(
                language="ru",
                category=self.list_of_data[message.chat.id]["category"],
                q=self.list_of_data[message.chat.id]["q"],
                sources=self.list_of_data[message.chat.id]["sources"])
        for i in range(
                len(self.list_of_data[message.chat.id]['top_headlines']
                    ['articles'])):
            self.send_message(
                message.chat.id,
                f'''[Посмотреть]({self.list_of_data[message.chat.id]['top_headlines']["articles"][i]["url"]})''',
                parse_mode='MarkdownV2',
                reply_markup=markup)
        if len(self.list_of_data[message.chat.id]['top_headlines']
               ['articles']) == 0:
            self.send_message(
                message.chat.id,
                "По вашему запросу ничего не найдено. Попробуйте другой запрос, или подождите некоторое время, когда новости по вашим параметрам появятся, или вы можете воспользоватся функцией поиска всех новостей за более давний строк. По этой функцией вы не можете задать категорию новостей, только источник и/или ключевое слово. Также вы не можете по этой функцией отправить запрос по умолчанию, хотя 1 пункт должен быть задан настройкой не по умолчанию. Нажмите на /more_news, чтобы воспользоватся данной функцией",
                reply_markup=markup)
        else:
            self.send_message(
                message.chat.id,
                "Если вы хотите получить больше новостей, то попробуйте другой запрос, или подождите некоторое время, когда новости по вашим параметрам появятся, или вы можете воспользоватся функцией поиска всех новостей за более давний строк. По этой функцией вы не можете задать категорию новостей, только источник и/или ключевое слово. Нажмите на /more_news, чтобы воспользоватся данной функцией",
                reply_markup=markup)

    def get_news3(self, message: telebot.types.Message):
        if self.list_of_data[message.chat.id]["more_news"] is False:
            self.count = 0
            self.list_of_data[message.chat.id]["more_news"] = True
            self.list_of_data[
                message.chat.id]["sources_more_news"] = self.list_of_data[
                    message.chat.id]["sources"]
            self.q_more_news = self.list_of_data[message.chat.id]["q"]
        markup = markup = self.buttons2()
        button3 = telebot.types.KeyboardButton("Получить новости")
        markup.add(button3)
        self.send_message(
            message.chat.id,
            "Вы попали в раздел поиска всех новостей по вашим параметрам. Вы можете задать источник и/или ключевое слово. Параметры в этом разделе поиска копируются с параметрами запроса общего поиска, но при изменении их в этом разделе, они не будут сохранены в параметры общего поиска. Если вы хотите изменить параметры запроса, нажмите на кнопки ниже, иначе нажмите на кнопку 'Получить новости'",
            reply_markup=markup)
        self.send_message(
            message.chat.id, f"""Запрос задан по следующим параметрам:
1. Источник: {next((key for key, value in self.list_of_sorces.items() if value == self.list_of_data[message.chat.id]["sources_more_news"]))}
2. Ключевое слово: {self.list_of_data[message.chat.id]["q_more_news"] if self.list_of_data[message.chat.id]["q_more_news"] is not None else "Без ключевого слова"}"""
        )

    def get_news4(self, message: telebot.types.Message):
        if self.list_of_data[message.chat.id][
                "sources_more_news"] is None and self.list_of_data[
                    message.chat.id]["q_more_news"] is None:
            self.send_message(
                message.chat.id,
                "Вы не задали источник и ключевое слово. Задайте хотя бы 1 параметр, чтобы получить новости"
            )
        else:
            self.list_of_data[message.chat.id]["more_news"] = False
            markup = self.buttons(message)
            buttonsp = telebot.types.KeyboardButton("/news")
            markup.add(buttonsp)
            self.list_of_data[
                message.chat.id]["all_articles"] = self.newsapi.get_everything(
                    sources=self.list_of_data[
                        message.chat.id]["sources_more_news"],
                    q=self.list_of_data[message.chat.id]["q_more_news"])
            if len(self.list_of_data[message.chat.id]["all_articles"]
                   ['articles']) <= 20:
                for i in range(
                        len(self.list_of_data[message.chat.id]["all_articles"]
                            ['articles'])):
                    self.send_message(
                        message.chat.id,
                        f'[Посмотреть]({self.list_of_data[message.chat.id]["all_articles"]["articles"][i]["url"]})',
                        parse_mode='MarkdownV2',
                        reply_markup=markup)
                self.send_message(message.chat.id,
                                  "Все новости выведены.",
                                  reply_markup=markup)
            elif len(self.list_of_data[message.chat.id]["all_articles"]
                     ['articles']) > 20:
                buttonsp2 = telebot.types.KeyboardButton(
                    "Получить еще новости")
                markup.add(buttonsp2)
                for i in range(20):
                    self.send_message(
                        message.chat.id,
                        f'[Посмотреть]({self.list_of_data[message.chat.id]["all_articles"]["articles"][i]["url"]})',
                        parse_mode='MarkdownV2',
                        reply_markup=markup)
                self.list_of_data[message.chat.id]["count"] += 20
                self.send_message(
                    message.chat.id,
                    f"""По вашему запросу было найдено {len(self.list_of_data[message.chat.id]["all_articles"]['articles'])} новостей. Сейчас было выведено 20 новостей. Если вы хотите получить еще новости, нажмите на кнопку 'Получить еще новости'. При нажатии на любую другую кнопку, вы выходите из раздела поиска всех новостей.""",
                    reply_markup=markup)
            elif len(self.list_of_data[message.chat.id]["all_articles"]
                     ['articles']) == 0:
                self.send_message(
                    message.chat.id,
                    "По вашему запросу ничего не найдено. Попробуйте другой запрос.",
                    reply_markup=markup)

    def get_news5(self, message: telebot.types.Message):
        for i in range(self.list_of_data[message.chat.id]["count"],
                       self.list_of_data[message.chat.id]["count"] + 20):
            self.send_message(
                message.chat.id,
                f'[Посмотреть]({self.list_of_data[message.chat.id]["all_articles"]["articles"][i]["url"]})',
                parse_mode='MarkdownV2')
            if self.list_of_data[message.chat.id]["all_articles"]["articles"][
                    i] == self.list_of_data[
                        message.chat.id]["all_articles"]["articles"][-1]:
                break
        self.list_of_data[message.chat.id]["count"] += 20
        if self.list_of_data[message.chat.id]["count"] < len(self.list_of_data[
                message.chat.id]["all_articles"]['articles']):
            self.send_message(
                message.chat.id,
                f"""Осталось {len(self.list_of_data[message.chat.id]["all_articles"]['articles']) - self.list_of_data[message.chat.id]["count"]} новостей. Нажмите на кнопку 'Получить еще новости', чтобы вывести еще новостей"""
            )
        else:
            self.list_of_data[message.chat.id]["count"] = 0
            markup = self.buttons(message)
            self.send_message(message.chat.id,
                              "Все новости выведены.",
                              reply_markup=markup)

    def set_sorces(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Google News (Russia)")
        button2 = telebot.types.KeyboardButton("Лента.ру")
        button3 = telebot.types.KeyboardButton("РБК")
        button4 = telebot.types.KeyboardButton("RT")
        button5 = telebot.types.KeyboardButton("Все источники")
        markup.add(button, button2, button3, button4, button5)
        self.send_message(message.chat.id,
                          "Выбирите источник",
                          reply_markup=markup)

    def set_sorces2(self, message: telebot.types.Message):
        if message.text in self.list_of_sorces and self.list_of_data[
                message.chat.id]["more_news"] is False:
            self.list_of_data[
                message.chat.id]["sources"] = self.list_of_sorces[message.text]
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            if self.list_of_data[message.chat.id]["sources"] is not None:
                button = telebot.types.KeyboardButton("Задать источник")
                button2 = telebot.types.KeyboardButton("Задать ключевое слово")
                button3 = telebot.types.KeyboardButton("/news")
                markup.add(button, button2, button3)
            else:
                button = telebot.types.KeyboardButton("Задать источник")
                button2 = telebot.types.KeyboardButton("Задать категорию")
                button3 = telebot.types.KeyboardButton("Задать ключевое слово")
                button4 = telebot.types.KeyboardButton("/news")
                markup.add(button, button2, button3, button4)
            self.send_message(
                message.chat.id,
                "Источник задан. Если вы хотите указать категорию, то верните значение источника по умолчанию, иначе вы можете нажать на кнопку /news.",
                reply_markup=markup)
        elif message.text in self.list_of_sorces and self.list_of_data[
                message.chat.id]["more_news"] is True:
            self.list_of_data[message.chat.id][
                "sources_more_news"] = self.list_of_sorces[message.text]
            markup = self.buttons2()
            button3 = telebot.types.KeyboardButton("/more_news")
            markup.add(button3)
            self.send_message(message.chat.id,
                              "Источник задан.",
                              reply_markup=markup)

    def set_category(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Бизнес")
        button2 = telebot.types.KeyboardButton("Наука")
        button3 = telebot.types.KeyboardButton("Технологии")
        button4 = telebot.types.KeyboardButton("Здоровье")
        button5 = telebot.types.KeyboardButton("Спорт")
        button6 = telebot.types.KeyboardButton("Развлечения")
        button7 = telebot.types.KeyboardButton("Общие")
        button8 = telebot.types.KeyboardButton("Все категории")
        markup.add(button, button2, button3, button4, button5, button6,
                   button7, button8)
        self.send_message(message.chat.id,
                          "Выбирите категорию",
                          reply_markup=markup)

    def set_category2(self, message: telebot.types.Message):
        if message.text in self.list_of_categorys:
            self.list_of_data[message.chat.id][
                "category"] = self.list_of_categorys[message.text]
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            if self.list_of_data[message.chat.id]["category"] is not None:
                button = telebot.types.KeyboardButton("Задать категорию")
                button2 = telebot.types.KeyboardButton("Задать ключевое слово")
                button3 = telebot.types.KeyboardButton("/news")
                markup.add(button, button2, button3)
            else:
                button = telebot.types.KeyboardButton("Задать источник")
                button2 = telebot.types.KeyboardButton("Задать категорию")
                button3 = telebot.types.KeyboardButton("Задать ключевое слово")
                button4 = telebot.types.KeyboardButton("/news")
                markup.add(button, button2, button3, button4)
            self.send_message(
                message.chat.id,
                "Категория задана. Если вы хотите указать источник, то верните значение по умолчанию, иначе вы можете нажать на кнопку /news.",
                reply_markup=markup)

    def set_q(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["flag_for_q"] = True
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton(
            "Без ключевого слова - по умолчанию")
        markup.add(button)
        self.send_message(message.chat.id,
                          "Введите ключевое слово",
                          reply_markup=markup)

    def set_q2(self, message: telebot.types.Message):
        self.list_of_data[message.chat.id]["flag_for_q"] = False
        if message.text == "Без ключевого слова - по умолчанию" and self.list_of_data[
                message.chat.id]["more_news"] is False:
            self.list_of_data[message.chat.id]["q"] = None
        elif message.text != "Без ключевого слова - по умолчанию" and self.list_of_data[
                message.chat.id]["more_news"] is False:
            self.list_of_data[message.chat.id]["q"] = message.text
        elif message.text == "Без ключевого слова - по умолчанию" and self.list_of_data[
                message.chat.id]["more_news"] is True:
            self.list_of_data[message.chat.id]["q_more_news"] = None
        elif message.text != "Без ключевого слова - по умолчанию" and self.list_of_data[
                message.chat.id]["more_news"] is True:
            self.list_of_data[message.chat.id]["q_more_news"] = message.text
        if self.list_of_data[message.chat.id]["more_news"] is False:
            markup = self.buttons(message)
            buttonsp = telebot.types.KeyboardButton("/news")
            markup.add(buttonsp)
            self.send_message(
                message.chat.id,
                "Ключевое слово задано. Если вы хотите указать источник или категорию, то нажмите на кнопки ниже, иначе вы можете нажать на кнопку /news.",
                reply_markup=markup)
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            self.buttons2()
            button3 = telebot.types.KeyboardButton("/more_news")
            markup.add(button3)
            self.send_message(message.chat.id,
                              "Ключевое слово задано.",
                              reply_markup=markup)

    def run(self):
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.get_news, commands=["news"])
        self.register_message_handler(
            self.get_news2,
            func=lambda message: message.text == 'Получить новости' and self.
            list_of_data[message.chat.id]["more_news"] is False)
        self.register_message_handler(self.get_news3, commands=["more_news"])
        self.register_message_handler(
            self.get_news4,
            func=lambda message: message.text == 'Получить новости' and self.
            list_of_data[message.chat.id]["more_news"] is True)
        self.register_message_handler(
            self.get_news5,
            func=lambda message: message.text == 'Получить еще новости')
        self.register_message_handler(
            self.set_sorces,
            func=lambda message: message.text == 'Задать источник')
        self.register_message_handler(
            self.set_sorces2,
            func=lambda message: message.text in self.list_of_sorces)
        self.register_message_handler(
            self.set_category,
            func=lambda message: message.text == 'Задать категорию')
        self.register_message_handler(
            self.set_category2,
            func=lambda message: message.text in self.list_of_categorys)
        self.register_message_handler(
            self.set_q,
            func=lambda message: message.text == 'Задать ключевое слово')
        self.register_message_handler(
            self.set_q2,
            func=lambda message: True and self.list_of_data[message.chat.id][
                "flag_for_q"] is True)
        self.polling(none_stop=True, interval=0)

