from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from config import bot2

TOKEN = bot2
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет ! Я WeatherBot, я могу показать погоду в вашем городе !'
                         'введите команду /weather город что-бы узнать погоду в заданном городе.')

@dp.message_handler(commands=['weather'])
async def pogoda(message: types.Message):

    com, city = message.text.split()

    appid = "2575577d56de4b432b9f55e7ea62c992"
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()

    if res.status_code == 200:
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        wind = data['wind']['speed']
        vis = data['visibility']

        message_text = (f'Город: {city}\n'
                        f'Погода: {weather}\n'
                        f'Температура: {temp}\n'
                        f'Скорость ветра: {wind}\n'
                        f'Видимость: {vis}')
        await message.reply(message_text)
    else:
        await message.answer('Извините, но что-то пошло не так. Введите название города ещё раз')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)