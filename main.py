from NewsBot import NewsBot
from NewsBotForChannel import NewsBotForChannel
from threading import Thread


def main() -> None:
    bot = NewsBotForChannel('6781204411:AAHxbmARcWtjT-dBcdTJqubLpuI1LG3-SfE')
    bot2 = NewsBot('6781204411:AAHxbmARcWtjT-dBcdTJqubLpuI1LG3-SfE')
    Thread(target=bot2.run()).start()
    bot.run()


if __name__ == "__main__":
    main()
