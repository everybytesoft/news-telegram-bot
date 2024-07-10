import telebot
from newsapi import NewsApiClient


class NewsBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.newsapi = NewsApiClient(api_key='24e1e7ae37b7406f9d529f9859172fa4')
        self.category = None
        self.q = None
        self.sources = None

    
    def start_command(self, message: telebot.types.Message):
        self.send_message(message.chat.id, "Привет! Я бот, который будет отправлять тебе новости по любой теме из главных новостей мира и твоей страны." )
        self.send_message(message.chat.id, """Вы можете задать:
1. Категорию новостей:
business, entertainment, general, health, science, sports, technology. По умолчанию все категории.
2. Ключевое слово: любое слово на вашем языке. По умолчанию без ключевого слова.
3. Источники: любой источник, написанное на английском языке и маленькими буквами без капсов. Если название источника состоит из нескольких слов, то нужно писать их через тире без пробелов. К примеру: bbc-news, cnn, meduza и т.д. По умолчанию все источники.""")
        self.send_message(message.chat.id, "Параметр источников нельзя указывать вместе с ключевым словом и категорией. Либо источник, либо категория и/или ключевое слово.")
        self.send_message(message.chat.id, "Чтобы получить новости, выбирете команду /news")
        self.send_message(message.chat.id, """Но перед тем как выбрать команду, введите через пробел сначало источники, затем категорию, затем ключевое слово. Если какой-то параметр не нужен, то напишите 'нет'. 
Пример: bbc-news нет нет""")

    
    def get_news(self, message: telebot.types.Message):
        top_headlines = self.newsapi.get_top_headlines(language="ru", category=self.category, q=self.q, sources=self.sources)
        print(len(top_headlines['articles']))
        for i in range(len(top_headlines['articles'])):
            self.send_message(message.chat.id, top_headlines["articles"][i]['title'])
            self.send_message(message.chat.id, top_headlines["articles"][i]['url'])
        if len(top_headlines['articles']) == 0:
            self.send_message(message.chat.id, "По вашему запросу ничего не найдено. Попробуйте другой запрос или подождите некоторое время, когда новости по вашим параметрам появятся.")
        self.category = None
        self.q = None
        self.sources = None
        self.send_message(message.chat.id, "Все параметры сброшены по умолчанию. Чтобы получить новости, введите снова параметры и выбирите команду /news")


    def get_text(self, message: telebot.types.Message):
        message_text = message.text.lower()
        list_of_parametres = message_text.split()
        if len(list_of_parametres) != 3:
            self.send_message(message.chat.id, "Неверный формат ввода. Попробуйте еще раз.")
        elif list_of_parametres[0] != "нет" and (list_of_parametres[1] != "нет" or list_of_parametres[2] != "нет"):
            self.send_message(message.chat.id, "Неверный формат ввода. Попробуйте еще раз.")
        else:
            list_of_parametres[0].replace(" ", "")
            list_of_parametres[1].replace(" ", "")
            list_of_parametres[2].replace(" ", "")
            if list_of_parametres[0] != "нет":
                self.sources = list_of_parametres[0]
            if list_of_parametres[1] != "нет":
                self.category = list_of_parametres[1]
            if list_of_parametres[2] != "нет":
                self.q = list_of_parametres[2]
            self.send_message(message.chat.id, "Теперь выбирите команду /news")
        
    def run(self):
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.get_news, commands=["news"])
        self.register_message_handler(self.get_text, content_types=["text"])
        self.polling(none_stop=True, interval=0)


    
