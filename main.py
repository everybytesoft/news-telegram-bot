import asyncio
from NewsBot import NewsBot
from NewsBotForChannel_ru import NewsBotForChannel_ru


async def main() -> None:
    bot = NewsBot('6781204411:AAHxbmARcWtjT-dBcdTJqubLpuI1LG3-SfE')
    bot2 = NewsBotForChannel_ru(
        '6781204411:AAHxbmARcWtjT-dBcdTJqubLpuI1LG3-SfE')

    # Запускаем оба бота параллельно
    await asyncio.gather(
        bot2.run(),
        bot.run(),
    )


if __name__ == "__main__":
    asyncio.run(main())
