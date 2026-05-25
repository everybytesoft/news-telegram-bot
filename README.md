# News Telegram Bot

[🇷🇺 Русский](#русский) | [🇬🇧 English](#english)

---

## Русский

Telegram-бот для получения актуальных новостей на русском языке. Состоит из двух компонентов:

- **NewsBot** — интерактивный бот для личных чатов: пользователь может настраивать фильтры (источник, категория, ключевое слово) и получать новости по запросу.
- **NewsBotForChannel_ru** — бот для автоматической публикации новостей в Telegram-канале каждый час.

### Стек

- Python 3.10+
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) — асинхронная работа с Telegram Bot API
- [newsdataapi](https://newsdata.io/docs) — получение новостей через NewsData.io API

### Установка

```bash
git clone <url>
cd News-telegram-bot-main
pip install -r requirements.txt
```

### Настройка

Откройте [main.py](main.py) и замените токены бота и ID канала на свои:

```python
# main.py
bot = NewsBot("ВАШ_ТОКЕН_БОТА")
bot2 = NewsBotForChannel_ru("ВАШ_ТОКЕН_БОТА")
```

```python
# NewsBotForChannel_ru.py
task2 = asyncio.create_task(self.send_news(-1002748974907))  # замените на ID вашего канала
```

Также замените API-ключ NewsData.io в обоих файлах ботов:

```python
self.newsapi = NewsDataApiClient(apikey="ВАШ_API_КЛЮЧ")
```

API-ключ можно получить бесплатно на [newsdata.io](https://newsdata.io).

### Запуск

```bash
python main.py
```

### Команды NewsBot

| Команда | Описание |
|---|---|
| `/start` | Запустить бота |
| `/set_sources` | Установить источники новостей |
| `/set_category` | Выбрать категорию |
| `/set_keyword` | Задать ключевое слово |
| `/get_filters` | Посмотреть текущие фильтры |
| `/get_news` | Получить новости |

---

## English

A Telegram bot for fetching up-to-date news in Russian. It consists of two components:

- **NewsBot** — an interactive bot for private chats: users can configure filters (source, category, keyword) and request news on demand.
- **NewsBotForChannel_ru** — a bot that automatically posts news to a Telegram channel every hour.

### Stack

- Python 3.10+
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) — async Telegram Bot API wrapper
- [newsdataapi](https://newsdata.io/docs) — news fetching via NewsData.io API

### Installation

```bash
git clone <url>
cd News-telegram-bot-main
pip install -r requirements.txt
```

### Configuration

Open [main.py](main.py) and replace the bot tokens and channel ID with your own:

```python
# main.py
bot = NewsBot("YOUR_BOT_TOKEN")
bot2 = NewsBotForChannel_ru("YOUR_BOT_TOKEN")
```

```python
# NewsBotForChannel_ru.py
task2 = asyncio.create_task(self.send_news(-1002748974907))  # replace with your channel ID
```

Also replace the NewsData.io API key in both bot files:

```python
self.newsapi = NewsDataApiClient(apikey="YOUR_API_KEY")
```

You can get a free API key at [newsdata.io](https://newsdata.io).

### Running

```bash
python main.py
```

### NewsBot Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/set_sources` | Set news sources |
| `/set_category` | Choose a category |
| `/set_keyword` | Set a keyword filter |
| `/get_filters` | View current filters |
| `/get_news` | Fetch news |
