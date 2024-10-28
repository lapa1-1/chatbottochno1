import telebot
import requests

bot = telebot.TeleBot('7260423453:AAHFsWqcL9gCH52NiwiBe8jF_f9-ft4TMps')  # Токен из BotFather

@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, "Здравствуйте! Как вас зовут?")
    bot.register_next_step_handler(sent, get_service)

def get_service(message):
    global user_name
    user_name = message.text  # Сохраняем имя пользователя

    user_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    user_markup.row('Березовын листья', 'Палочки')
    sent = bot.send_message(message.chat.id, "Какие услуги вас интересуют?", reply_markup=user_markup)
    bot.register_next_step_handler(sent, request_phone)

def request_phone(message):
    global service_type
    service_type = message.text  # Сохраняем выбранную услугу

    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = telebot.types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, 'Оставьте ваш контактный номер, чтобы наш менеджер смог связаться с вами.', reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def save_contact(message):
    if message.contact:  # Проверяем, что пользователь отправил контакт
        phone_number = message.contact.phone_number
        user_id = message.from_user.id

        # Отправка данных на сервер
        url = 'http://127.0.0.1:5000/api/submit'
        data = {
            "user_id": user_id,
            "phone_number": phone_number
        }
        response = requests.post(url, json=data)

        # Сообщаем пользователю о результате
        if response.status_code == 201:
            bot.send_message(message.chat.id, 'Ваш номер сохранен.')
        elif response.status_code == 200:
            bot.send_message(message.chat.id, 'Ваш номер уже существует в базе. Ожидайте вызов оператора.')
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка на сервере.')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте номер телефона.')

if __name__ == '__main__':
    bot.polling(none_stop=True)
