from aiogram import Bot, Dispatcher, executor, types
import modules.settings as sett

telegram_api = sett.telegram_api
bot = Bot(token=telegram_api)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    response_chat = f'{str(message.chat.id)}\n\nПривет!\nЭто id нашего с тобой чата!\nОн нужен в дальнейшем.\n'
    print(response_chat)
    await message.reply(response_chat)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
