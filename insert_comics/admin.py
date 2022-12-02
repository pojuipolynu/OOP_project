from comics_database import Comic
import telebot
from telebot import custom_filters
from telebot import types

comics_db = Comic("localhost", "root", "password", "database")

TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)

admin_id = [123456]
btn_list = ['title', 'author', 'artist', 'genre', 'periodicity', 'magazine',
            'chapters', 'status', 'colorization', 'kind', 'adaptation', 'translation', 'end']
periodicity_list = ['every day', 'every week', 'every month', 'non-periodical']
kind_list = ['manga', 'manhwa', 'manhua', 'comics', 'maliopys']
status_list = ['frozen', 'ongoing', 'completed']
colorization_list = ['monochrome', 'non-monochrome', 'lineart']
adaptation_list = ['film', 'cartoon', 'tvshow', 'show', 'anime']
author = ['name', 'surname', 'add']
answer_dict = {}


def generate_buttons(button_list, markup):
    for button in button_list:
        markup.add(types.KeyboardButton(button))
    return markup


def create_keyboards(button_list, width=2):
    markup = types.ReplyKeyboardMarkup(row_width=width)
    markup = generate_buttons(button_list, markup)
    return markup


@bot.message_handler(chat_id=admin_id, commands=['start'])
def admin_start(message):
    bot.send_message(
        message.chat.id, "You are allowed to use commands as admin.\nUse /help to see all commands.")


@bot.message_handler(commands=['start'])
def not_admin_start(message):
    bot.send_message(message.chat.id, "Hello! Let's start.")


@bot.message_handler(chat_id=admin_id, commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id, "/insert - add new comics\n/delete - delete comics\n/update - update comics\n/print - print information about comics")


@bot.message_handler(chat_id=admin_id, commands=['insert'])
def insert_command(message):
    answer_dict.clear()
    markup = create_keyboards(btn_list)
    bot.reply_to(message, "Insert comics.", reply_markup=markup)
    bot.register_next_step_handler(message, bot_asks)


@bot.message_handler(chat_id=admin_id, commands=['print'])
def print_command(message):
    bot.reply_to(message, "Enter title of comics to print it")
    bot.register_next_step_handler(message, print_in_database)
            
            

#delete part

@bot.message_handler(chat_id=admin_id, commands=['delete'])
def delete_command(message):
    bot.reply_to(message, "Enter title of comic to delete it")
    bot.register_next_step_handler(message, in_database)


def delete_comics(message, value):
    key = [value]
    bot.reply_to(message, 'Comics was deleted')
    comics_db.delete_comic(key)

@bot.message_handler(chat_id=admin_id)
def in_database(message):
    key = message.text.lower()
    if comics_db.search_comics([key]):
        bot.reply_to(message, 'Do you want to delete this comic? (yes or no)')
        bot.register_next_step_handler(message, delete_or_not, key)
    elif message.text == '/delete':
        delete_command(message)
    else:
        bot.reply_to(message, "Sorry, I don't find your comic.\n\nIf you want to try againt enter /delete.")
    
@bot.message_handler(chat_id=admin_id)
def delete_or_not(message, key):
    value = message.text.lower()
    if value == 'yes':
        delete_comics(message, key)
    elif value == '/delete':
        delete_command(message)
    elif value == 'no':
        bot.reply_to(message, "If you want to try againt enter /delete.")
    else:
        bot.reply_to(message, "I don't recognize your command.\n\nIf you want to try againt enter /delete.")

#delete part end







#print part starts

def print_info(mylist):
    title = f'Title: {mylist[0]}\n'
    chapters = f'Chapters: {mylist[1]}\n'
    author = f'Author: {mylist[2]} {mylist[3]}\n'
    artist = f'Artist: {mylist[4]} {mylist[5]}\n'
    kind = f'Kind: {mylist[6]}\n'
    genre = f'Genre: {mylist[8]}, {mylist[7]}\n'
    periodicity = f'Periodicity: {mylist[9]}\n'
    magazine = f'Magazine: {mylist[10]}\n'
    status = f'Status: {mylist[11]}\n'
    colorization = f'Colorization: {mylist[12]}\n'
    adaptation = f'Adaptation: {mylist[13]}\n'
    translation = f'Translation: {mylist[14]} ({mylist[15]})\n'
    return f'{title}{chapters}{author}{artist}{kind}{genre}{periodicity}{magazine}{status}{colorization}{adaptation}{translation}'

def print_comic(message):
    key = [message.text]
    row = comics_db.print_comics(key)
    bot.reply_to(message, print_info(row[0]))

@bot.message_handler(chat_id=admin_id)
def print_in_database(message):
    key = message.text.lower()
    if comics_db.search_comics([key]):
        print_comic(message)
    elif message.text == '/print':
        print_command(message)
    else:
        bot.reply_to(message, "Sorry, I don't find your comic.\n\nYou can /insert it or try /print again")

#print part ends










def return_to_main(message, key):
    store_answer(message, key)
    markup = create_keyboards(btn_list)
    bot.reply_to(message, 'Choose what you want to add', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def store_answer(message, key):
    comics_db.insert_comics(message.text, key, answer_dict)
    print(answer_dict)
    bot.register_next_step_handler(message, bot_asks)

@bot.message_handler(chat_id=admin_id)
def incorrect_message(message):
    bot.reply_to(message, "I don't recognize your messege")
    bot.register_next_step_handler(message, bot_asks)


@bot.message_handler(chat_id=admin_id)
def end(message):
    comics_db.insert_all(answer_dict)
    bot.reply_to(message, "The end of inserting")


@bot.message_handler(chat_id=admin_id)
def quation(message, quation, key):
    bot.reply_to(message, quation)
    bot.register_next_step_handler(message, store_answer, key)


@bot.message_handler(chat_id=admin_id)
def quation_choose(message, button_list, quation, key):
    markup = create_keyboards(button_list)
    message = bot.reply_to(message, quation, reply_markup=markup)
    bot.register_next_step_handler(message, return_to_main, key)


def bot_asks(message):
    value = message.text
    if value == 'title':
        quation(message, "Enter title of comics", value)
    elif value == 'author':
        quation(message, "Enter author's surname of comics", value)
    elif value == 'artist':
        quation(message, "Enter artist's surname of comics", value)
    elif value == 'genre':
        quation(message, "Enter genre of comics", value)
    elif value == 'periodicity':
        quation_choose(message, periodicity_list,
                       'Choose periodicity of comics', value)
    elif value == 'magazine':
        quation(message, "Enter magazine", value)
    elif value == 'chapters':
        quation(message, "Enter number of comics' chapters", value)
    elif value == 'status':
        quation_choose(message, status_list, 'Choose status of comics', value)
    elif value == 'colorization':
        quation_choose(message, colorization_list,
                       'Choose colorization', value)
    elif value == 'kind':
        quation_choose(message, kind_list, 'Choose kind of comics', value)
    elif value == 'adaptation':
        quation_choose(message, adaptation_list, 'Choose colorization', value)
    elif value == 'translation':
        quation(message, "Enter translation", value)
    elif value == '/insert':
        insert_command(message)
    elif message.text == 'end':
        end(message)
    else:
        incorrect_message(message)



bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()
