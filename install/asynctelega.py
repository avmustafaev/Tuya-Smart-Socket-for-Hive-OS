import sys

sys.path.insert(0, "./")

from aiogram import Bot, Dispatcher, executor, types
import modules.loadenvi as sett



telegram_api = sett.telegram_api
bot = Bot(token=telegram_api)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    response_chat = f"{str(message.chat.id)}\n\nПривет!\nЭто id нашего с тобой чата!\nОн нужен в дальнейшем.\n"
    print(response_chat)
    await message.reply(response_chat)


@dp.message_handler(commands=["pause"])
async def send_pause(message: types.Message):
    if int(message.chat.id) == int(sett.telegram_chat_id):
        sett.pauseunpause("pause")
        response_chat = "Обработчик на паузе!"
        print(response_chat)
    else:
        response_chat = "Не авторизован ты!"
    await message.reply(response_chat)


@dp.message_handler(commands=["unpause"])
async def send_unpause(message: types.Message):
    if int(message.chat.id) == int(sett.telegram_chat_id):
        sett.pauseunpause("unpause")
        response_chat = "Обработчик активирован!"
        print(response_chat)
    else:
        response_chat = "Не авторизован ты!"
    await message.reply(response_chat)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
