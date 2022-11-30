import telebot
from telebot import custom_filters
from telebot import types 

TOKEN = '5795242325:AAG3Ua6fD-ffCIQoP8_7Bg9IPDRmNithCvY'

bot = telebot.TeleBot(TOKEN)

admin_id = [520973029]
btn_list = ['Title', 'Author', 'Artist', 'Genre', 'Periodicity', 'Magazine', 'Chapters', 'Status', 'Colorization', 'Kind', 'Adaptation', 'Translation', 'Stop']
answer_dict = {}


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
def title_quation(message):
	bot.reply_to(message, "Enter title of comics")
	bot.register_next_step_handler(message, store_answer, 'name')

@bot.message_handler(chat_id=admin_id)
def author_quation(message):
	bot.reply_to(message, "Enter author of comics")
	bot.register_next_step_handler(message, store_answer, 'author')

@bot.message_handler(chat_id=admin_id)
def artist_quation(message):
	bot.reply_to(message, "Enter artist of comics")
	bot.register_next_step_handler(message, store_answer, 'artist')

@bot.message_handler(chat_id=admin_id)
def genre_quation(message):
	bot.reply_to(message, "Enter genre of comics")
	bot.register_next_step_handler(message, store_answer, 'genre')

@bot.message_handler(chat_id=admin_id)
def magazine_quation(message):
	bot.reply_to(message, "Enter magazine")
	bot.register_next_step_handler(message, store_answer, 'magazine')

@bot.message_handler(chat_id=admin_id)
def periodicity_quation(message):
	periodicity_list = ['every day', 'every week', 'every month', 'non-periodical']
	markup = create_keyboards(periodicity_list)
	message = bot.reply_to(message, 'Choose periodicity of comics', reply_markup=markup)
	bot.register_next_step_handler(message, return_to_main, 'periodicity')
	

@bot.message_handler(chat_id=admin_id)
def kind_quation(message):
	kind_list = ['manga', 'manhwa', 'manhua', 'comics', 'maliopys']
	markup=create_keyboards(kind_list)
	message = bot.reply_to(message, 'Choose kind of comics', reply_markup=markup)
	bot.register_next_step_handler(message, return_to_main, 'kind')

def return_to_main(message, key):
	store_answer(message, key)
	markup = create_keyboards(btn_list)
	bot.reply_to(message, "Continue...", reply_markup=markup)
	bot.register_next_step_handler(message, bot_asks)


@bot.message_handler(chat_id=admin_id)
def incorrect_message(message):
	bot.reply_to(message, "I don't recognize your messege")
	bot.register_next_step_handler(message, bot_asks)

@bot.message_handler(chat_id=admin_id)
def chapters_quation(message):
	bot.reply_to(message, "Enter number of comics' chapters")
	bot.register_next_step_handler(message, store_answer, 'chapter')

@bot.message_handler(chat_id=admin_id)
def status_quation(message):
	status_list = ['frozen', 'ongoing', 'completed']
	markup = create_keyboards(status_list)
	message = bot.reply_to(message, 'Choose status of comics', reply_markup=markup)
	bot.register_next_step_handler(message, return_to_main, 'status')

@bot.message_handler(chat_id=admin_id)
def colorization_quation(message):
	colorization_list = ['monochrome', 'non-monochrome', 'lineart']
	markup = create_keyboards(colorization_list)
	message = bot.reply_to(message, 'Choose colorization', reply_markup=markup)
	bot.register_next_step_handler(message, return_to_main, 'colorization')

@bot.message_handler(chat_id=admin_id)
def adaptation_quation(message):
	adaptation_list = ['film', 'cartoon', 'tvshow', 'show', 'anime']
	markup = create_keyboards(adaptation_list)
	message = bot.reply_to(message, 'Choose colorization', reply_markup=markup)
	bot.register_next_step_handler(message, return_to_main, 'adaptation')


@bot.message_handler(chat_id=admin_id)
def stop(message):
	bot.reply_to(message, "The end of inserting")


def bot_asks(message):
	if message.text == 'Title':
		title_quation(message)
	elif message.text == 'Author':
		author_quation(message)
	elif message.text == 'Artist':
		artist_quation(message)
	elif message.text == 'Genre':
		genre_quation(message)
	elif message.text == 'Periodicity':
		periodicity_quation(message)
	elif message.text == 'Magazine':
		magazine_quation(message)
	elif message.text == 'Chapters':
		chapters_quation(message)
	elif message.text == 'Status':
		status_quation(message)
	elif message.text == 'Colorization':
		colorization_quation(message)
	elif message.text == 'Kind':
		kind_quation(message)
	elif message.text == 'Adaptation':
		adaptation_quation(message)
	elif message.text == 'Translation':
		magazine_quation(message)
	elif message.text == 'Stop':
		stop(message)
	else:
		incorrect_message(message)

bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()



