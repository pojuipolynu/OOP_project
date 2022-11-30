import telebot
from telebot import custom_filters
from telebot import types 

TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)

admin_id = [12345]
btn_list = ['Title', 'Author', 'Artist', 'Genre', 'Periodicity', 'Magazine', 'Chapters', 'Status', 'Colorization', 'Kind', 'Adaptation', 'Translation', 'Stop']
answer_dict = {}
periodicity_list = ['every day', 'every week', 'every month', 'non-periodical']
kind_list = ['manga', 'manhwa', 'manhua', 'comics', 'maliopys']
status_list = ['frozen', 'ongoing', 'completed']
colorization_list = ['monochrome', 'non-monochrome', 'lineart']
adaptation_list = ['film', 'cartoon', 'tvshow', 'show', 'anime']


@bot.message_handler(chat_id=admin_id, commands=['start']) 
def admin_start(message):
    bot.send_message(message.chat.id, "You are allowed to use commands as admin.\nUse /help to see all commands.")

@bot.message_handler(commands=['start'])
def not_admin_start(message):
    bot.send_message(message.chat.id, "Hello! Let's start.")

@bot.message_handler(chat_id=admin_id, commands=['help']) 
def help_command(message):
    bot.send_message(message.chat.id, "/insert - add new comics\n/delete - delete comics\n/update - update comics")

@bot.message_handler(chat_id=admin_id, commands=['insert'])
def insert_command(message):
	markup = create_keyboards(btn_list)
	bot.reply_to(message, "Insert comics.", reply_markup=markup)
	bot.register_next_step_handler(message, bot_asks)

def create_keyboards(button_list, width=2):
	markup = types.ReplyKeyboardMarkup(row_width=width)
	markup = generate_buttons(button_list, markup)
	return markup

def return_to_main(message, key):
	store_answer(message, key)
	markup = create_keyboards(btn_list)
	bot.reply_to(message, 'Choose what you want to add', reply_markup=markup)
	
@bot.message_handler(content_types=['text'])
def store_answer(message, key):
	answer_dict[key] = message.text
	print(answer_dict)
	bot.register_next_step_handler(message, bot_asks)

def generate_buttons(button_list, markup):
    for button in button_list:
        markup.add(types.KeyboardButton(button))
    return markup

@bot.message_handler(chat_id=admin_id)
def incorrect_message(message):
	bot.reply_to(message, "I don't recognize your messege")
	bot.register_next_step_handler(message, bot_asks)

@bot.message_handler(chat_id=admin_id)
def stop(message):
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
	if message.text == 'Title':
		quation(message, "Enter title of comics", 'name')
	elif message.text == 'Author':
		quation(message, "Enter author of comics", 'author')
	elif message.text == 'Artist':
		quation(message, "Enter artist of comics", 'artist')
	elif message.text == 'Genre':
		quation(message, "Enter genre of comics", 'genre')
	elif message.text == 'Periodicity':
		quation_choose(message, periodicity_list, 'Choose periodicity of comics', 'periodicity')
	elif message.text == 'Magazine':
		quation(message, "Enter magazine", 'magazine')
	elif message.text == 'Chapters':
		quation(message, "Enter number of comics' chapters", 'chapter')
	elif message.text == 'Status':
		quation_choose(message, status_list, 'Choose status of comics', 'status')
	elif message.text == 'Colorization':
		quation_choose(message, colorization_list, 'Choose colorization', 'colorization')
	elif message.text == 'Kind':
		quation_choose(message, kind_list, 'Choose kind of comics', 'kind')
	elif message.text == 'Adaptation':
		quation_choose(message, adaptation_list, 'Choose colorization', 'adaptation')
	elif message.text == 'Translation':
		quation(message, "Enter translation", 'translation')
	elif message.text == 'Stop':
		stop(message)
	else:
		incorrect_message(message)

bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()

