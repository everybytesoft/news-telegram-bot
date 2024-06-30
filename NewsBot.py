import telebot
from newsapi import NewsApiClient


class NewsBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.newsapi = NewsApiClient(api_key='24e1e7ae37b7406f9d529f9859172fa4')


    def start_command(self, message: telebot.types.Message):
        self.send_message(message.chat.id, "Привет! Я бот, который будет отправлять тебе новости по определенной темы, источника, категории, языка и страны." )


    def get_news(self, message: telebot.types.Message):
        top_headlines = self.newsapi.get_top_headlines(category='sports',
                                                        language='ru')

        for i in range(len(top_headlines['articles'])):
            self.send_message(message.chat.id, top_headlines['articles'][i]['title'])
            if top_headlines['articles'][i]['description'] != None:
                self.send_message(message.chat.id, top_headlines['articles'][i]['description'])
            self.send_message(message.chat.id, top_headlines['articles'][i]['url'])


    def run(self):
        self.register_message_handler(self.start_command, commands=["start"])
        self.register_message_handler(self.get_news, commands=["news"])
        self.polling(none_stop=True, interval=0)
