import telebot
from newsapi import NewsApiClient
from time import sleep
from threading import Thread
import re
from bs4 import BeautifulSoup
import requests


class NewsBotForChannel_ru(telebot.TeleBot):

  def __init__(self, token):
    super().__init__(token)
    self.newsapi = NewsApiClient(api_key='24e1e7ae37b7406f9d529f9859172fa4')
    self.list_of_used_news = []
    self.flag = True
    self.flag2 = True

  def escape_md(self, text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

  def escape_md_text_link(self, text: str) -> str:
    escape_chars = r'\)'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

  def send_news(self, Chat_id):
    while True:
      top_headlines = self.newsapi.get_top_headlines(language="ru" )
      for i in range(len(top_headlines['articles'])):
        if top_headlines["articles"][i]["url"] not in self.list_of_used_news:
          data = top_headlines['articles'][i]
          title = self.escape_md(data['title'])
          url = self.escape_md_text_link(data['url'])
          response = requests.get(url)
          if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image = soup.find("meta", property="og:image")
            if image:
              self.send_photo(Chat_id,
                              image['content'],
                              f'[{title}]({url})',
                              parse_mode='MarkdownV2')
            else:
              url2 = url[8:]
              url_link = url[:8] + url2[:url2.find("/")]
              response = requests.get(url_link)
              if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                image = soup.find("meta", property="og:image")
                if image:
                  self.send_photo(Chat_id,
                    image['content'],
                    f'[{title}]({url_link})',
                    parse_mode='MarkdownV2')
                else:
                  print("Нет картинки")
              else:
                print(f"Не удалось загрузить страницу. Код ошибки: {response.status_code}")
          else:
            url2 = url[8:]
            url_link = url[:8] + url2[:url2.find("/")]
            response = requests.get(url_link)
            if response.status_code == 200:
              soup = BeautifulSoup(response.content, 'html.parser')
              image = soup.find("meta", property="og:image")
              if image:
                self.send_photo(Chat_id,
                  image['content'],
                  f'[{title}]({url_link})',
                  parse_mode='MarkdownV2')
              else:
                print("Нет картинки")
            else:
              print(f"Не удалось загрузить страницу. Код ошибки: {response.status_code}")
          self.list_of_used_news.append(top_headlines["articles"][i]["url"])
      sleep(900)

  def Clear_list(self):
    while True:
      sleep(86400)
      del self.list_of_used_news[0:len(self.list_of_used_news) - 20]

  def run(self):
    Thread(target=self.Clear_list).start()
    self.send_news(-1002147192937)
    self.polling(none_stop=True, interval=0)
