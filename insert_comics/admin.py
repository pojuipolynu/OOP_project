from comics_database import Comic
import telebot
from telebot import custom_filters
from telebot import types

comics_db = Comic("localhost", "root", "vfhsyf10", "comics1")

TOKEN = '5795242325:AAG3Ua6fD-ffCIQoP8_7Bg9IPDRmNithCvY'

bot = telebot.TeleBot(TOKEN)

admin_id = [520973029]
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
    bot.send_message(message.chat.id, "You are allowed to use commands as admin.\nUse /help to see all commands.")


@bot.message_handler(commands=['start'])
def not_admin_start(message):
    bot.send_message(message.chat.id, "Hello! Let's start.")


@bot.message_handler(chat_id=admin_id, commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id, "/insert - add new comics\n/delete - delete comics\n/update - update comics\n/print - print information about comics")


@bot.message_handler(chat_id=admin_id, commands=['insert'])
def insert_command(message):
    command = 1
    answer_dict.clear()
    markup = create_keyboards(btn_list)
    bot.reply_to(message, "Insert comics.", reply_markup=markup)
    bot.register_next_step_handler(message, bot_asks, command)

@bot.message_handler(chat_id=admin_id, commands=['update'])
def update_command(message):
    answer_dict.clear()
    bot.reply_to(message, "Update comics. Enter name of comics.")
    bot.register_next_step_handler(message, update_in_database)

def enter_update(message, key1):
    command = 2
    markup = create_keyboards(btn_list)
    bot.reply_to(message, "Update comics. Choose what you want to update.", reply_markup=markup)
    bot.register_next_step_handler(message, bot_asks, command, key1)


@bot.message_handler(chat_id=admin_id)
def update_in_database(message):
    key = message.text.lower()
    if comics_db.search_comics([key]):
        key1 = comics_db.search_comics([key])
        enter_update(message, key1)
    elif message.text == '/update':
        update_command(message)
    else:
        bot.reply_to(message, "Sorry, I don't find your comic.\n\nYou can /insert it or try /update again")


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
    genre = f'Genre: {mylist[8]}\n'
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

#insert part starts

'''
def store_answer(message, key):
    insert_comics(message, key, answer_dict)
    print(answer_dict)
    bot.register_next_step_handler(message, bot_asks)
@bot.message_handler(chat_id=admin_id)
def incorrect_message(message):
    bot.reply_to(message, "I don't recognize your messege")
    bot.register_next_step_handler(message, )

'''

@bot.message_handler(chat_id=admin_id)
def quation(message, quation, key, commmand, key1):
    bot.reply_to(message, quation)
    bot.register_next_step_handler(message, insert_comics, key, commmand, key1)


@bot.message_handler(chat_id=admin_id)
def quation_choose(message, button_list, quation, key, commmand, key1):
    markup = create_keyboards(button_list)
    message = bot.reply_to(message, quation, reply_markup=markup)
    bot.register_next_step_handler(message, return_to_main, key, button_list, commmand, key1)

def return_to_main(message, key, button_list, command, key1):
    if message.text.lower() not in button_list: #don't work
        quation_choose(message, button_list, "You can't choose this answer. Try again!", key)
    insert_comics(message, key, command, key1)
    markup = create_keyboards(btn_list)
    bot.reply_to(message, 'Choose what you want to add', reply_markup=markup)

@bot.message_handler(chat_id=admin_id)
def next_choose(message, command, key1):
    bot.reply_to(message, "Chose what you want to add.")
    bot.register_next_step_handler(message, bot_asks, command, key1)

@bot.message_handler(chat_id=admin_id)
def end(message, command):
    if command == 1:
        comics_db.insert_all(answer_dict)
        bot.reply_to(message, "The end of inserting")
    else:
        bot.reply_to(message, "The end of updating")

'''
def not_digits(message,key):
    if key == 'chapters':
        if not message.text.isdigit() or int(message.text) <= 0:
            quation(message, "Chapters is number", key)
    else:
        return message
    bot.register_next_step_handler(message, insert_comics, key)
'''


@bot.message_handler(chat_id=admin_id)
def bot_asks(message, command, key1=None):
    value = message.text
    if value == 'title':
        quation(message, "Enter title of comics", value, command, key1)
    elif value == 'author':
        quation(message, "Enter author's surname of comics", value, command, key1)
    elif value == 'artist':
        quation(message, "Enter artist's surname of comics", value, command, key1)
    elif value == 'genre':
        quation(message, "Enter genre of comics", value, command, key1)
    elif value == 'periodicity':
        quation_choose(message, periodicity_list,
                       'Choose periodicity of comics', value, command, key1)
    elif value == 'magazine':
        quation(message, "Enter magazine", value, command, key1)
    elif value == 'chapters':
        quation(message, "Enter number of comics' chapters", value, command, key1)
    elif value == 'status':
        quation_choose(message, status_list, 'Choose status of comics', value, command, key1)
    elif value == 'colorization':
        quation_choose(message, colorization_list,
                       'Choose colorization', value, command, key1)
    elif value == 'kind':
        quation_choose(message, kind_list, 'Choose kind of comics', value, command, key1)
    elif value == 'adaptation':
        quation_choose(message, adaptation_list, 'Choose adaptation', value, command, key1)
    elif value == 'translation':
        quation(message, "Enter language", value, command, key1)
    elif value == '/insert':
        insert_command(message)
    elif value == '/update':
        update_command(message)
    elif value == '/delete':
        delete_command(message)
    elif value == '/print':
        print_command(message)
    elif value == 'end':
        end(message, command)
    else:
        next_choose(message, command, key1)

@bot.message_handler(chat_id=admin_id)
def insert_comics(message, choice, command, key1):
    key = message.text.lower()
    keyl = list()
    keyl.append(key)
    if choice == 'title':
        if command == 1:
            answer_dict['name'] = comics_db.select_name(key)
        else:
            comics_db.update_name(key, key1)
    elif choice == 'genre':
        if comics_db.search_genre(keyl):
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (comics_db.search_genre(keyl))])
            else:
                comics_db.update_genre(keyl, key1)    
        else:
            comics_db.insert_genre(keyl)
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (comics_db.search_genre(keyl))])
            else:
                comics_db.update_genre(keyl, key1)    
    elif choice == 'author':
        if comics_db.search_author(keyl):
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (comics_db.search_author(keyl))])
            else:
               comics_db.update_author(keyl, key1) 
        else:
            extra_not_in_base(message, "It seems that your author is not in our database.\nPlease help us by entering his name!\n", keyl, choice, command, key1)
    elif choice == 'artist':
        if comics_db.search_artist(keyl):
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (comics_db.search_artist(keyl))])
            else:
               comics_db.update_artist(keyl, key1) 
        else:
            extra_not_in_base(message, "It seems that your artist is not in our database.\nPlease help us by entering his name!\n", keyl, choice, command, key1)
    elif choice == 'periodicity':
        if command == 1:
            answer_dict[choice] = ([x[0] for x in (comics_db.select_period(key, keyl))])
        else:
            comics_db.update_period(key, keyl, key1)
    elif choice == 'magazine':
        if comics_db.search_magazine(keyl):
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (comics_db.search_magazine(keyl))])
            else:
                comics_db.update_magazine(key, key1)
        else:
            magazine_extra(message, keyl, choice, command, key1)
    elif choice == 'chapters':
        if command == 1:
            answer_dict[choice] = comics_db.select_num(int(key))
        else:
            comics_db.update_num(key, key1)
    elif choice == 'status':
        if command == 1:
            answer_dict[choice] = ([x[0] for x in (comics_db.select_status(key, keyl))])
        else:
            comics_db.update_status(key, keyl, key1)
    elif choice == 'colorization':
        if command == 1:
            answer_dict[choice] = ([x[0] for x in (comics_db.select_color(key, keyl))])
        else:
            comics_db.update_color(key, keyl, key1)
    elif choice == 'kind':
        if command == 1:
            answer_dict[choice] = ([x[0] for x in (comics_db.select_kind(key, keyl))])
        else:
            comics_db.update_kind(key, keyl, key1)
    elif choice == 'adaptation':
        if command == 1:
            answer_dict[choice] = ([x[0] for x in (comics_db.select_adapt(key, keyl))])
        else:
            comics_db.update_adapt(key, keyl, key1)
    elif choice == 'translation':
        translation_legality(message, keyl, choice, command, key1)
    else:
        raise TypeError
    #bot.reply_to(message, "Chose what you want to add.")
    bot.register_next_step_handler(message, bot_asks, command, key1)
    print(answer_dict)

#author and artist
@bot.message_handler(chat_id=admin_id)
def extra_not_in_base(message, quation, keyl, choice, command, key1=None, extra=None):
    bot.reply_to(message, quation)
    bot.register_next_step_handler(message, extra_insert, keyl, choice, command, key1, extra)

# magazine
@bot.message_handler(chat_id=admin_id)
def magazine_extra(message, keyl, choice, command, key1=None):
    bot.reply_to(message, "It seems that your magazine is not in our database. Please help us by entering its circulation!\n")
    bot.register_next_step_handler(message, magazine_periodicity, keyl, choice, command, key1)

@bot.message_handler(chat_id=admin_id)
def magazine_periodicity(message, keyl, choice, command, key1):
    circ = message.text
    markup = create_keyboards(periodicity_list)
    bot.reply_to(message, "Thank you! Also enter, please, its periodicity!\n", reply_markup=markup)
    bot.register_next_step_handler(message, extra_insert, keyl, choice, command, key1, circ)

# translation
@bot.message_handler(chat_id=admin_id)
def translation_legality(message, keyl, choice, command, key1=None):
    bot.reply_to(message, "Is your translation official or non-official?")
    bot.register_next_step_handler(message, translate_select, keyl, choice, command, key1)

@bot.message_handler(chat_id=admin_id)
def translation_status(message, keyl, choice, command, key1, leg):
    markup = create_keyboards(status_list)
    bot.reply_to(message, "Also enter, please, what's your translation status?\n", reply_markup=markup)
    bot.register_next_step_handler(message, extra_insert, keyl, choice, command, key1, leg)

def translate_select(message, keyl, choice, command, key1):
    leg = message.text
    if comics_db.search_translation(keyl, leg):
        if command == 1:
            answer_dict[choice] = ([x[0] for x in (comics_db.search_translation(keyl, leg))])
        else:
            comics_db.update_trans(keyl, key1, leg)
    else: 
        translation_status(message, keyl, choice, command, key1, leg)

@bot.message_handler(chat_id=admin_id)
def extra_insert(message, keyl, choice, command, key1, extra):
    if choice == 'author':
        comics_db.insert_author(message.text.lower(), keyl)
        bot.reply_to(message, "Author was insert")
    elif choice == 'artist':
        comics_db.insert_artist(message.text.lower(), keyl)
        bot.reply_to(message, "Artist was insert")
    elif choice == 'translation':
        st = message.text
        markup = create_keyboards(btn_list)
        bot.reply_to(message, 'Translation was inserted', reply_markup=markup)
        se = list()
        se.append(st)
        comics_db.insert_translation(keyl, extra, comics_db.select_status(st, se))
    elif choice == 'magazine':
        period = message.text
        markup = create_keyboards(btn_list)
        bot.reply_to(message, 'Magazine was inserted', reply_markup=markup)
        se = list()
        se.append(period)
        comics_db.insert_magazine(keyl, extra, comics_db.select_period(period, se))
    if command == 1:
        select_something(message, keyl, choice, extra)
    else:
        update_something(message, keyl, choice, key1, extra)



def select_something(message, keyl, choice, leg):
    if choice == 'author':
        answer_dict[choice] =  ([x[0] for x in (comics_db.search_author(keyl))])
    elif choice == 'artist':
        answer_dict[choice] = ([x[0] for x in (comics_db.search_artist(keyl))])
    elif choice == 'translation':
        answer_dict[choice] = ([x[0] for x in (comics_db.search_translation(keyl, leg))])
    elif choice == 'magazine':
        answer_dict[choice] = ([x[0] for x in (comics_db.search_magazine(keyl))])

def update_something(message, keyl, choice, key1, leg):
    if choice == 'author':
        comics_db.update_author(keyl, key1)
    elif choice == 'artist':
        comics_db.update_artist(keyl, key1)
    elif choice == 'translation':
        comics_db.update_trans(keyl, key1, leg)
    elif choice == 'magazine':
        comics_db.update_magazine(keyl, key1)
    print('Updated')

#insert part ends

bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()



