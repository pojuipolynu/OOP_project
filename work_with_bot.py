import telebot
from telebot import custom_filters
from telebot import types 
TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)

admin_id = [1234]
admin_dict = {}

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
	bot.send_message(message.chat.id, "Insert comics.\nEnter title of comics.")
	admin_dict['message.chat.id'] = 0
	bot.register_next_step_handler(message.chat.id, bot_asks)

@bot.message_handler(chat_id=admin_id)
def author_quation(message):
	bot.reply_to(message, "Enter author of comics")
	admin_dict['message'] = 1
	bot.register_next_step_handler(message, bot_asks)

@bot.message_handler(chat_id=admin_id)
def artist_quation(message):
	bot.reply_to(message, "Enter artist of comics")
	admin_dict['message'] = 2
	bot.register_next_step_handler(message, bot_asks)

@bot.message_handler(chat_id=admin_id)
def magazine_quation(message):
	bot.reply_to(message, "Enter magazine of comics")
	admin_dict['message'] = 3
	bot.register_next_step_handler(message, bot_asks)

@bot.message_handler(chat_id=admin_id)
def status_quation(message):
	markup = types.InlineKeyboardMarkup()
	buttonA = types.InlineKeyboardButton('ongoing', callback_data='ongoing')
	buttonB = types.InlineKeyboardButton('completed', callback_data='completed')
	buttonC = types.InlineKeyboardButton('frozen', callback_data='frozen')
	markup.row(buttonA, buttonB, buttonC)
	message = bot.reply_to(message, 'Choose status of comics', reply_markup=markup)
	admin_dict['message'] = 4
	bot.register_next_step_handler(message, bot_asks)



def bot_asks(message):
	if admin_dict['message']==0:
		author_quation(message)
	elif admin_dict['message']==1:
		artist_quation(message)
	elif admin_dict['message']==2:
		magazine_quation(message)
	elif admin_dict['message']==3:
		status_quation(message)


bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()





