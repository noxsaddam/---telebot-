import telebot
import config
from telebot import types
from pprint import pprint
from comb import combination
import requests
import datetime

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.first_name.capitalize() in ["Алексей", "Леха", "Алеша"]:
        bot.send_message(message.chat.id, 'Тебе Алеша оно не поможет, попей лучше пивка!')
    mess = f"Добро пожаловать <b>{message.from_user.first_name}</b>!"

    # keybord
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/check_combinations")
    item2 = types.KeyboardButton("/weather")
    item3 = types.KeyboardButton("/start")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, "Помогу посмотреть ваши комбинации, для этого нажмите chek_combinations\n"
                                      "или дам сводку по погоде - нажмите weather")


@bot.message_handler(commands=["check_combinations"])
def pocket_cards(message):
    markup1 = types.ForceReply(selective=False)
    card_request = bot.send_message(message.chat.id,
                                    f'Какие карты у Вас на руках?\nВ формате "Ак 6б"([Значение][Масть])'
                                    , reply_markup=markup1)
    bot.register_next_step_handler(card_request, search)


@bot.message_handler(commands=['weather'])
def weather(massage):
    weather_request = bot.send_message(massage.chat.id, "В каком городе узнать погоду?")
    bot.register_next_step_handler(weather_request, get_weather)

def get_weather(massage):
    try:
        weather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={massage.text}&appid={config.open_weather_token}&units=metric")
        # f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric")
        weather = weather.json()

        name_city = weather['name']
        temp = weather['main']['temp']
        temp_feels_like = weather['main']['feels_like']
        pressure = weather['main']['pressure']
        humidity = weather['main']['humidity']
        wind = weather['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(weather['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(weather['sys']['sunset'])
        message = f"----{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}----\n" \
                  f"Погода в городе: {name_city}\nТемпература: {temp}°C\nОщущается как: {temp_feels_like}°C\n" \
                  f"Влажность: {humidity}%\nДавление: {pressure}мм рт. ст.\nВетер: {wind}м/с\n" \
                  f"Восход солнца: {sunrise}\nЗакат: {sunset}\nСветовой день: {sunset - sunrise}"
        bot.send_message(massage.chat.id, message)

    except:
        bot.send_message(massage.chat.id, "Проверте название города")


@bot.message_handler(content_types=['text'])
def test(message):
    bot.send_message(message.chat.id, "Я могу помочь с картами или погодой, а с этим не могу")


def search(message):
    bot.send_message(message.chat.id, f"OK\n{message.text}")
    cards = message.text
    print(cards)
    markup2 = types.InlineKeyboardMarkup(row_width=2)
    preflop = types.InlineKeyboardButton("Preflop", callback_data=f"pref+{cards}")
    flop = types.InlineKeyboardButton("Flop", callback_data=f"flop+{cards}")
    tern = types.InlineKeyboardButton("Tern", callback_data=f"tern+{cards}")
    river = types.InlineKeyboardButton("River", callback_data=f"river+{cards}")
    markup2.add(preflop, flop, tern, river)
    bot.send_message(message.chat.id, "Какая стадия игры?", reply_markup=markup2)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            data = call.data.split("+")[0]
            cards = call.data.split("+")[1].split()
            with open('cards.txt', 'w') as entry:
                entry.writelines(" ".join(cards))

            if data == "pref":
                bot.send_message(call.message.chat.id, combination(cards))

                # Удаление кнопок после нажатия
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Результат:", reply_markup=None)
            elif data in ["flop", "tern", "river"]:
                card_request_table = bot.send_message(call.message.chat.id, "Какие карты на столе?")
                bot.register_next_step_handler(card_request_table, input_cards_table)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Стадия игры - {data.capitalize()}:", reply_markup=None)
            # elif data == "tern":
            #     bot.send_message(call.message.chat.id, "Шансы терна")
            # elif data == "river":
            #     bot.send_message(call.message.chat.id, "Шансы ривера")
            else:
                bot.send_message(call.message.chat.id, "Что то мне невидомое")

            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                       text="Результат:", reply_markup=None)

    except Exception as e:
        print(repr(e))


def input_cards_table(message):
    with open("cards.txt", 'r') as reading:
        cards = reading.read().split()

    cards_table = message.text.split()
    bot.send_message(message.chat.id, f"<b>{combination(cards, cards_table)}</b>", parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("/check_combinations")
    item2 = types.KeyboardButton("/weather")
    markup.add(item, item2)
    bot.send_message(message.chat.id, "Поссмотрть другую руку?\n Или узнать погоду?", reply_markup=markup)


bot.polling(none_stop=True)
