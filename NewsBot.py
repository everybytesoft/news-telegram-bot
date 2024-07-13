import telebot
from newsapi import NewsApiClient


class NewsBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.newsapi = NewsApiClient(
            api_key='24e1e7ae37b7406f9d529f9859172fa4')
        self.category = None
        self.q = None
        self.sources = None
        self.list_of_sorces = {
            "Google News (Russia) - по умолчанию": None,
            "Лента.ру": 'lenta',
            "РБК": 'rbc',
            "RT": 'rt'
        }
        self.list_of_categorys = {
            "Бизнес": 'business',
            "Развлечения": 'entertainment',
            "Общие - по умолчанию": None,
            "Здоровье": 'health',
            "Наука": 'science',
            "Спорт": 'sports',
            "Технологии": 'technology'
        }

    
    def start_command(self, message: telebot.types.Message):
        self.category = None
        self.q = None
        self.sources = None
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
1. Источники: По умолчанию Google News (Russia) - все источники.
2. Категорию новостей: По умолчанию общие - все категории.
3. Ключевое слово: любое слово на вашем языке. По умолчанию без ключевого слова."""
        )
        self.send_message(
            message.chat.id,
            "Параметр источников нельзя указывать вместе категорией. Либо источник, либо категория."
        )
        self.send_message(message.chat.id,
                          "Чтобы узнать найстроки параметров и получить новости, выбирете команду /news")

    
    def get_news(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.sources is not None:
            button = telebot.types.KeyboardButton("Задать источник")
            button2 = telebot.types.KeyboardButton("Задать ключевое слово")
            button3 = telebot.types.KeyboardButton("Получить новости")
            markup.add(button, button2, button3)
        elif self.category is not None:
            button = telebot.types.KeyboardButton("Задать категорию")
            button2 = telebot.types.KeyboardButton("Задать ключевое слово")
            button3 = telebot.types.KeyboardButton("Получить новости")
            markup.add(button, button2, button3)
        else:
            button = telebot.types.KeyboardButton("Задать источник")
            button2 = telebot.types.KeyboardButton("Задать категорию")
            button3 = telebot.types.KeyboardButton("Задать ключевое слово")
            button4 = telebot.types.KeyboardButton("Получить новости")
            markup.add(button, button2, button3, button4)
        self.send_message(message.chat.id, f"""Запрос задан по следующим параметрам:
1. Источник: {next((key for key, value in self.list_of_sorces.items() if value == self.sources))}
2. Категория: {next((key for key, value in self.list_of_categorys.items() if value == self.category))}
3. Ключевое слово: {self.q if self.q is not None else "Без ключевого слова"}""")
        self.send_message(message.chat.id, "Если вы хотите изменить параметры запроса, нажмите на кнопки ниже, иначе нажмите на кнопку 'Получить новости'", reply_markup=markup)

    def get_news2(self, message: telebot.types.Message):
        top_headlines = self.newsapi.get_top_headlines(language="ru",
            category=self.category,
            q=self.q,
            sources=self.sources)
        for i in range(len(top_headlines['articles'])):
            self.send_message(
        message.chat.id,
        f'[Посмотреть]({top_headlines["articles"][i]["url"]})',
        parse_mode='MarkdownV2')
        if len(top_headlines['articles']) == 0:
            self.send_message(message.chat.id,
        "По вашему запросу ничего не найдено. Попробуйте другой запрос или подождите некоторое время, когда новости по вашим параметрам появятся.")

        
    def set_sorces(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Google News (Russia) - по умолчанию")
        button2 = telebot.types.KeyboardButton("Лента.ру")
        button3 = telebot.types.KeyboardButton("РБК")
        button4 = telebot.types.KeyboardButton("RT")
        markup.add(button, button2, button3, button4)
        self.send_message(message.chat.id,
                          "Выбирите источник",
                          reply_markup=markup)

    def set_sorces2(self, message: telebot.types.Message):
        message_text = message.text
        if message_text in self.list_of_sorces:
            self.sources = self.list_of_sorces[message_text]
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            if self.sources is not None:
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
            self.send_message(message.chat.id,
                              "Источник задан. Если вы хотите указать категорию, то верните значение источника по умолчанию, иначе вы можете нажать на кнопку /news.",
                              reply_markup=markup)

    
    def set_category(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Бизнес")
        button2 = telebot.types.KeyboardButton("Наука")
        button3 = telebot.types.KeyboardButton("Технологии")
        button4 = telebot.types.KeyboardButton("Здоровье")
        button5 = telebot.types.KeyboardButton("Спорт")
        button6 = telebot.types.KeyboardButton("Развлечения")
        button7 = telebot.types.KeyboardButton("Общие - по умолчанию")
        markup.add(button, button2, button3, button4, button5, button6,
                   button7)
        self.send_message(message.chat.id,
                          "Выбирите категорию",
                          reply_markup=markup)

    def set_category2(self, message: telebot.types.Message):
        message_text = message.text
        if message_text in self.list_of_categorys:
            self.category = self.list_of_categorys[message_text]
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            if self.category is not None:
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
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Без ключевого слова - по умолчанию")
        markup.add(button)
        self.send_message(message.chat.id, "Введите ключевое слово", reply_markup=markup)

    def set_q2(self, message: telebot.types.Message):
        if message.text == "Без ключевого слова - по умолчанию":
            self.q = None
        else:
            self.q = message.text
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.sources is not None:
            button = telebot.types.KeyboardButton("Задать источник")
            button2 = telebot.types.KeyboardButton("Задать ключевое слово")
            button3 = telebot.types.KeyboardButton("/news")
            markup.add(button, button2, button3)
        elif self.category is not None:
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
                "Ключевое слово задано. Если вы хотите указать источник или категорию, то нажмите на кнопки ниже, иначе вы можете нажать на кнопку /news.",
                reply_markup=markup)

        
    def run(self):
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.get_news, commands=["news"])
        self.register_message_handler(
            self.get_news2,
            func=lambda message: message.text == 'Получить новости')
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
            func=lambda message: message.text != 'Задать ключевое слово' and
            message.text != 'Задать категорию' and message.text !=
            'Задать источник' and message.text not in self.list_of_sorces and
            message.text not in self.list_of_categorys and message.text != "Получить новости")
        self.polling(none_stop=True, interval=0)



    
