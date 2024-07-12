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
            "Google News (Russia)": None,
            "Лента.ру": 'lenta',
            "РБК": 'rbc',
            "RT": 'rt'
        }
        self.list_of_categorys = {
            "Бизнес": 'business',
            "Развлечение": 'entertainment',
            "Общее": 'general',
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
        button = telebot.types.KeyboardButton("/news")
        button2 = telebot.types.KeyboardButton("Задать источник")
        button3 = telebot.types.KeyboardButton("Задать категорию")
        button4 = telebot.types.KeyboardButton("Задать ключевое слово")
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
            "Параметр источников нельзя указывать вместе с ключевым словом и категорией. Либо источник, либо категория и/или ключевое слово."
        )
        self.send_message(message.chat.id,
                          "Чтобы получить новости, выбирете команду /news")
        self.send_message(
            message.chat.id,
            "Но перед тем, как получить новости, выбирите параметры запроса. Для этого нажмите на кнопки ниже(если настройки по умолчанию вас устраивает, то можете сразу нажать на кнопку /news)."
        )

    def get_news(self, message: telebot.types.Message):
        top_headlines = self.newsapi.get_top_headlines(language="ru",
                                                       category=self.category,
                                                       q=self.q,
                                                       sources=self.sources)
        for i in range(len(top_headlines['articles'])):
            self.send_message(
                message.chat.id,
                f'[Google]({top_headlines["articles"][i]["url"]})',
                parse_mode='MarkdownV2')
        if len(top_headlines['articles']) == 0:
            self.send_message(
                message.chat.id,
                "По вашему запросу ничего не найдено. Попробуйте другой запрос или подождите некоторое время, когда новости по вашим параметрам появятся."
            )
        self.category = None
        self.q = None
        self.sources = None
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("/news")
        button2 = telebot.types.KeyboardButton("Задать источник")
        button3 = telebot.types.KeyboardButton("Задать категорию")
        button4 = telebot.types.KeyboardButton("Задать ключевое слово")
        markup.add(button, button2, button3, button4)
        self.send_message(
            message.chat.id,
            "Все параметры сброшены по умолчанию. Чтобы получить новости, введите снова параметры и выбирите команду /news",
            reply_markup=markup)

    def set_sorces(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Google News (Russia)")
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
            button = telebot.types.KeyboardButton("/news")
            markup.add(button)
            self.send_message(message.chat.id,
                              "Источник задан. Теперь нажмите кнопку /news",
                              reply_markup=markup)

    def set_category(self, message: telebot.types.Message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Бизнес")
        button2 = telebot.types.KeyboardButton("Развлечение")
        button3 = telebot.types.KeyboardButton("Общее")
        button4 = telebot.types.KeyboardButton("Здоровье")
        button5 = telebot.types.KeyboardButton("Наука")
        button6 = telebot.types.KeyboardButton("Спорт")
        button7 = telebot.types.KeyboardButton("Технологии")
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
            button = telebot.types.KeyboardButton("Задать ключевое слово")
            button2 = telebot.types.KeyboardButton("/news")
            markup.add(button, button2)
            self.send_message(
                message.chat.id,
                "Категория задана. Вы можете задать ключевое слово или нажать на кнопку /news",
                reply_markup=markup)

    def set_q(self, message: telebot.types.Message):
        self.send_message(message.chat.id, "Введите ключевое слово")

    def set_q2(self, message: telebot.types.Message):
        self.q = message.text
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("Задать категорию")
        button2 = telebot.types.KeyboardButton("/news")
        markup.add(button, button2)
        self.send_message(
            message.chat.id,
            "Ключевое слово задано. Вы можете задать категорию или нажать на кнопку /news",
            reply_markup=markup)

    def run(self):
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.get_news, commands=["news"])
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
            message.text not in self.list_of_categorys)
        self.polling(none_stop=True, interval=0)


    
