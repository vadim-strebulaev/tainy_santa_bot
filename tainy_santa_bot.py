import telebot
import ast

bot = telebot.TeleBot('Сюда токен ложи')
names = dict()

BUTTONS = [
    "Загадать желание",
    "Я Федосеев",
    "Ввести имя",
    "Подтвердить готовность"
]

def go_save():
    global names

    file_path = "data_base.txt"
    with open(file_path, "w") as file:
        file.write(str(names))

def get_save():
    global names
    file_path = "data_base.txt"
    with open(file_path, "r") as file:
        local_names = file.readline()
    if local_names != "":
        local_names = ast.literal_eval(local_names)

        names = local_names
    else:
        names = {}



def create_buttons():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [telebot.types.KeyboardButton(topic) for topic in BUTTONS]
    keyboard.add(*buttons)
    return keyboard



@bot.message_handler(commands=['start'])
def start(message):
    get_save()
    global names

    if message.chat.id not in names:
        names[message.chat.id] = {"name": "NONAME", "wish": "NOWISH", "is_ready": False}
        go_save()

    keyboard = create_buttons()
    bot.send_message(message.chat.id, 'Привет! Выбери нужную тебе команду! (Федосеев не учавствует)', reply_markup=keyboard)
    



@bot.message_handler(func=lambda message: message.text == 'Я Федосеев')
def command_fedoseev(message):
    get_save() 
    global names

    keyboard = create_buttons()
    bot.send_message(message.chat.id, 'Оу...\nПрошу прощения, тебе нельзя учавстовать. \nПрости... \nС наступающим тебя!', reply_markup=keyboard)



@bot.message_handler(func=lambda message: message.text == 'Ввести имя')
def command_name(message):
    get_save() 
    global names

    bot.send_message(message.chat.id, 'Теперь введи своё имя и я добавлю тебя в базу данных!')
    
    bot.register_next_step_handler(message, process_name_step)

def process_name_step(message):
    get_save()
    global names

    chat_id = message.chat.id
    name = message.text
    if name == "NONAME":
        print("Такое нельзя!")
        return
    
    names[chat_id]["name"] = name
    keyboard = create_buttons()
    bot.send_message(chat_id, f"Ваше имя: {name}", reply_markup=keyboard)
    go_save()



@bot.message_handler(func=lambda message: message.text == 'Подтвердить готовность')
def command_ready(message):
    get_save() 
    global names

    keyboard = create_buttons()
    if names[message.chat.id]["name"] == "NONAME":
        bot.send_message(message.chat.id, "Сначала введи имя.", reply_markup=keyboard)

    elif names[message.chat.id]["wish"] == "NOWISH":
        bot.send_message(message.chat.id, "Сначала введи желание.", reply_markup=keyboard)

    else:
        bot.send_message(message.chat.id, 'О! Ты уже готов?\nХорошо!, когда все будут готовы, я запущу раздачу желаний.\nНо ты всё ещё сможешь поменять своё желание до момента раздачи.', reply_markup=keyboard)
        names[message.chat.id]["is_ready"] = True
    go_save()



@bot.message_handler(func=lambda message: message.text == 'Загадать желание')
def command_i_wonna(message):
    bot.send_message(message.chat.id, 'Напиши своё желание и я обновлю свою базу данных. Никто пока не сможет его увидеть.\nА пока до раздачи желаний ты сможешь его поменять.')

    bot.register_next_step_handler(message, process_wish)

def process_wish(message):
    get_save() 
    global names


    chat_id = message.chat.id
    wish = message.text
    if wish == "NOWISH":
        print("Такое нельзя!")
        return
    
    names[chat_id]["wish"] = wish

    keyboard = create_buttons()
    bot.send_message(chat_id, f"Ваше желание: {wish}", reply_markup=keyboard)
    go_save()



@bot.message_handler()
def start(message):
    get_save() 
    global names
    keyboard = create_buttons()
    bot.send_message(message.chat.id, "Команду пожалуйста введи.", reply_markup=keyboard)

try:
    bot.polling()

except:
    bot.polling()
