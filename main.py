from NewsBot import NewsBot
from NewsBotForChannel_ru import NewsBotForChannel_ru
from threading import Thread


def main() -> None:
    bot = NewsBot('6781204411:AAHxbmARcWtjT-dBcdTJqubLpuI1LG3-SfE')
    bot2 = NewsBotForChannel_ru('6781204411:AAHxbmARcWtjT-dBcdTJqubLpuI1LG3-SfE')
    Thread(target=bot.run).start()
    Thread(target=bot2.run).start()


if __name__ == "__main__":
    main()
