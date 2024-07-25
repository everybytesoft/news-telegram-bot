import telebot
from newsapi import NewsApiClient
from time import sleep
from threading import Thread


class NewsBotForChannel(telebot.TeleBot):

  def __init__(self, token):
    super().__init__(token)
    self.newsapi = NewsApiClient(api_key='24e1e7ae37b7406f9d529f9859172fa4')
    self.list_of_used_news = []
    self.flag = True
    self.flag2 = True

  def send_news(self, Chat_id):
    while True:
      top_headlines = self.newsapi.get_top_headlines(language="ru")
      for i in range(len(top_headlines['articles'])):
        if top_headlines["articles"][i]["url"] not in self.list_of_used_news:
          self.send_message(
              Chat_id,
              f'[Посмотреть]({top_headlines["articles"][i]["url"]})',
              parse_mode='MarkdownV2')
          self.list_of_used_news.append(top_headlines["articles"][i]["url"])
      sleep(900)

  def Clear_list(self):
    while True:
      sleep(86400)
      del self.list_of_used_news[0:len(self.list_of_used_news) - 20]

  def run(self):
    Thread(target=self.Clear_list).start()
    self.send_news(908324504)
    self.polling(none_stop=True, interval=0)
