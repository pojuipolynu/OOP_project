from _comics_database import Comic
import telebot
from telebot import custom_filters
from telebot import types

TOKEN = 'TOKEN'

admin_id = [1234]  # your telegram id

btn_list = ['title', 'author', 'artist', 'genre', 'periodicity', 'magazine',
            'chapters', 'status', 'colorization', 'kind', 'adaptation', 'translation', 'end', 'menu']
key_list = ['name', 'author', 'artist', 'genre', 'periodicity', 'magazine',
            'chapters', 'status', 'colorization', 'kind', 'adaptation', 'translation']
periodicity_list = ['every day', 'every week', 'every month', 'non-periodical']
kind_list = ['manga', 'manhwa', 'manhua', 'comics', 'maliopys']
status_list = ['frozen', 'ongoing', 'completed']
colorization_list = ['monochrome', 'non-monochrome', 'lineart']
adaptation_list = ['film', 'cartoon', 'tvshow', 'show', 'anime']
answer_dict = {}
saved = []
user_id = []
database_id = []
command_list = ['/start', '/help', '/insert', '/update', '/delete', '/search', '/sort', '/random', '/saved']

# insert part starts


class insert_update_class(menu_class):
    def insert_command(self, message):
        command = 1
        answer_dict.clear()
        markup = self.keyboard_insert()
        self.bot.reply_to(message, "Insert comics. Choose what you want to add.", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command)

    def update_command(self, message):
        answer_dict.clear()
        self.bot.reply_to(message, "Update comics. Enter name of comics.")
        self.bot.register_next_step_handler(message, self.update_in_database)

    def enter_update(self, message, key1):
        command = 2
        markup = self.keyboard_insert()
        self.print_comic(message)
        self.bot.reply_to(message, "Update comics. Choose what you want to update.", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)

    def update_in_database(self, message):
        key = message.text.lower()
        if self.comics_db.search_comics([key]):
            key1 = self.comics_db.search_comics([key])
            self.enter_update(message, key1)
        elif message.text == '/update':
            self.update_command(message)
        else:
            self.bot.reply_to(message, "Sorry, I don't find your comic.\n\nYou can /insert it or try /update again")

    def select_something(self, message, keyl, choice, leg):
        if choice == 'author':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_author(keyl))])
        elif choice == 'artist':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_artist(keyl))])
        elif choice == 'translation':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_translation(keyl, leg))])
        elif choice == 'magazine':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_magazine(keyl))])

    def update_something(self, message, keyl, choice, key1, leg):
        if choice == 'author':
            self.comics_db.update_author(keyl, key1)
        elif choice == 'artist':
            self.comics_db.update_artist(keyl, key1)
        elif choice == 'translation':
            self.comics_db.update_trans(keyl, key1, leg)
        elif choice == 'magazine':
            self.comics_db.update_magazine(keyl, key1)

    def quation(self, message, quation, key, commmand, key1):
        self.bot.reply_to(message, quation)
        self.bot.register_next_step_handler(message, self.insert_comics, key, commmand, key1)

    def quation_choose(self, message, button_list, quation, key, commmand, key1):
        markup = self.create_keyboards(button_list)
        message = self.bot.reply_to(message, quation, reply_markup=markup)
        self.bot.register_next_step_handler(message, self.insert_comics, key, commmand, key1)
        # bot.register_next_step_handler(message, return_to_main, key, button_list, commmand, key1)

    def incorrect_message(self, message, command, key1):
        self.bot.reply_to(message, "I don't recognize your messege.")
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)

    def check_key(self):
        answer_list = []
        not_in_answer = []
        for key in answer_dict:
            answer_list.append(key)
        for key1 in key_list:
            if key1 not in answer_list:
                not_in_answer.append(key1)
        return not_in_answer

    def end(self, message, command, key1):
        if command == 1:
            if self.check_key():
                key_l = self.check_key()
                self.bot.reply_to(message, ', '.join(map(str,
                                                         key_l)) + " wasn't add.\n\nChoose what you want to add.")
                self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
                return
            else:
                self.comics_db.insert_all(answer_dict)
                markup = self.menu_keyboard(message)
                self.bot.send_message(message.chat.id, "The end of inserting.\n\nChoose a command.",
                                      reply_markup=markup)
        else:
            markup = self.menu_keyboard(message)
            self.bot.send_message(message.chat.id, "The end of updating.\n\nChoose a command.", reply_markup=markup)

    def bot_asks(self, message, command, key1=None):
        value = message.text
        if value == 'title':
            self.quation(message, "Enter title of comics", value, command, key1)
        elif value == 'author':
            self.quation(message, "Enter author's surname of comics", value, command, key1)
        elif value == 'artist':
            self.quation(message, "Enter artist's surname of comics", value, command, key1)
        elif value == 'genre':
            self.quation(message, "Enter genre of comics", value, command, key1)
        elif value == 'periodicity':
            self.quation_choose(message, periodicity_list,
                           'Choose periodicity of comics', value, command, key1)
        elif value == 'magazine':
            self.quation(message, "Enter magazine", value, command, key1)
        elif value == 'chapters':
            self.quation(message, "Enter number of comics' chapters", value, command, key1)
        elif value == 'status':
            self.quation_choose(message, status_list, 'Choose status of comics', value, command, key1)
        elif value == 'colorization':
            self.quation_choose(message, colorization_list,
                           'Choose colorization', value, command, key1)
        elif value == 'kind':
            self.quation_choose(message, kind_list, 'Choose kind of comics', value, command, key1)
        elif value == 'adaptation':
            self.quation_choose(message, adaptation_list, 'Choose adaptation', value, command, key1)
        elif value == 'translation':
            self.quation(message, "Enter language", value, command, key1)
        elif value in command_list:
            self.command_choose(message, value)
        elif value == 'menu':
            self.menu_command(message)
        elif value == 'end':
            self.end(message, command, key1)
        else:
            self.incorrect_message(message, command, key1)

    def insert_comics(self, message, choice, command, key1):
        key = message.text.lower()
        if key in command_list:
            self.command_choose(message, key)
            return
        keyl = list()
        keyl.append(key)
        if choice == 'title':
            if command == 1:
                answer_dict['name'] = self.comics_db.select_name(key)
            else:
                self.comics_db.update_name(key, key1)
        elif choice == 'genre':
            if self.comics_db.search_genre(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_genre(keyl))])
                else:
                    self.comics_db.update_genre(keyl, key1)
            else:
                self.comics_db.insert_genre(keyl)
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_genre(keyl))])
                else:
                    self.comics_db.update_genre(keyl, key1)
        elif choice == 'author':
            if self.comics_db.search_author(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_author(keyl))])
                else:
                    self.comics_db.update_author(keyl, key1)
            else:
                self.extra_not_in_base(message,
                    "It seems that your author is not in our database.\nDo you want to insert it? (yes or no)\n",
                                  keyl, choice, command, key1)
                return
        elif choice == 'artist':
            if self.comics_db.search_artist(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_artist(keyl))])
                else:
                    self.comics_db.update_artist(keyl, key1)
            else:
                self.extra_not_in_base(message,
                    "It seems that your artist is not in our database.\nDo you want to insert it? (yes or no)\n",
                                  keyl, choice, command, key1)
                return
        elif choice == 'periodicity':
            if key not in periodicity_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_period(key, keyl))])
            else:
                self.comics_db.update_period(key, keyl, key1)
        elif choice == 'magazine':
            if self.comics_db.search_magazine(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_magazine(keyl))])
                else:
                    self.comics_db.update_magazine(key, key1)
            else:
                self.extra_not_in_base(message,
                                  "It seems that your magazine is not in our database.\nDo you want to insert it? (yes or no)\n",
                                  keyl, choice, command, key1)
                return
        elif choice == 'chapters':
            if not key.isdigit():
                self.bot.reply_to(message, "Chapters is number. Please try again.")
                self.bot.register_next_step_handler(message, self.insert_comics, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = self.comics_db.select_num(int(key))
            else:
                self.comics_db.update_num(key, key1)
        elif choice == 'status':
            if key not in status_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_status(key, keyl))])
            else:
                self.comics_db.update_status(key, keyl, key1)
        elif choice == 'colorization':
            if key not in colorization_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_color(key, keyl))])
            else:
                self.comics_db.update_color(key, keyl, key1)
        elif choice == 'kind':
            if key not in kind_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_kind(key, keyl))])
            else:
                self.comics_db.update_kind(key, keyl, key1)
        elif choice == 'adaptation':
            if key not in adaptation_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_adapt(key, keyl))])
            else:
                self.comics_db.update_adapt(key, keyl, key1)
        elif choice == 'translation':
            self.translation_legality(message, keyl, choice, command, key1)
            return
        else:
            raise TypeError
        markup = self.keyboard_insert()
        self.bot.reply_to(message, 'Choose what you want to add.', reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
        print(answer_dict)

    # author, artist and magazine
    def extra_not_in_base(self, message, quation, keyl, choice, command, key1=None, extra=None):
        self.bot.reply_to(message, quation)
        self.bot.register_next_step_handler(message, self.add_new_or_not, keyl, choice, command, key1, extra)

    def magazine_periodicity(self, message, keyl, choice, command, key1):
        circ = message.text
        if not circ.isdigit():
            self.bot.reply_to(message, "Circulation is number. Try again.\n")
            self.bot.register_next_step_handler(message, self.magazine_periodicity, keyl, choice, command, key1)
            return
        markup = self.create_keyboards(periodicity_list)
        self.bot.reply_to(message, "Thank you! Also enter, please, its periodicity!\n", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, circ)

    # translation
    def translation_legality(self, message, keyl, choice, command, key1=None):
        self.bot.reply_to(message, "Is your translation official or non-official?")
        self.bot.register_next_step_handler(message, self.translate_select, keyl, choice, command, key1)

    def translate_select(self, message, keyl, choice, command, key1):
        leg = message.text.lower()
        if leg not in ('official', 'non-official'):
            self.bot.reply_to(message, "Legality is official or non-official. Try again.\n")
            self.bot.register_next_step_handler(message, self.translate_select, keyl, choice, command, key1)
            return
        elif leg in command_list:
            self.command_choose(message, leg)
            return
        if self.comics_db.search_translation(keyl, leg):
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.search_translation(keyl, leg))])
            else:
                self.comics_db.update_trans(keyl, key1, leg)
            self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
        else:
            self.bot.reply_to(message,
                    "It seems that your translation is not in our database.\nDo you want to insert it? (yes or no)\n")
            self.bot.register_next_step_handler(message, self.add_new_or_not, keyl, choice, command, key1, leg)

    def add_new_or_not(self, message, keyl, choice, command, key1, extra):
        key = message.text.lower()
        if key == 'yes':
            if choice in ('author', 'artist'):
                self.bot.reply_to(message, 'Enter name:')
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
            elif choice == 'magazine':
                self.bot.reply_to(message, 'Enter circulation:')
                self.bot.register_next_step_handler(message, self.magazine_periodicity, keyl, choice, command, key1)
            elif choice == 'translation':
                markup = self.create_keyboards(status_list)
                self.bot.reply_to(message, "Enter translation status:\n", reply_markup=markup)
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
        elif key == 'no':
            markup = self.keyboard_insert()
            self.bot.reply_to(message, 'Choose what you want to add.', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
            return
        elif key in command_list:
            self.command_choose(message, key)
            return
        else:
            self.bot.reply_to(message, "I don't recognize your command. Try again!")
            self.bot.register_next_step_handler(message, self.add_new_or_not, keyl, choice, command, key1, extra)

    def extra_insert(self, message, keyl, choice, command, key1, extra):
        key = message.text.lower()
        if key in command_list:
            self.command_choose(message, key)
            return
        if choice == 'author':
            self.comics_db.insert_author(key, keyl)
        elif choice == 'artist':
            self.comics_db.insert_artist(key, keyl)
        elif choice == 'translation':
            if key not in status_list:
                self.bot.reply_to(message, "You can't choose this answer. Try again.")
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
                return
            se = list()
            se.append(key)
            self.comics_db.insert_translation(keyl, extra, self.comics_db.select_status(key, se))
        elif choice == 'magazine':
            if key not in periodicity_list:
                self.bot.reply_to(message, "You can't choose this answer. Try again.")
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
                return
            se = list()
            se.append(key)
            self.comics_db.insert_magazine(keyl, extra, self.comics_db.select_period(key, se))
        if command == 1:
            self.select_something(message, keyl, choice, extra)
        else:
            self.update_something(message, keyl, choice, key1, extra)
        markup = self.keyboard_insert()
        self.bot.reply_to(message, choice.capitalize() + ' was inserted. Choose what you want to add next.',
                     reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)


# chooses

# insert or update part ends

# delete part
class delete_class:
    def delete_command(self, message):
        self.bot.reply_to(message, "Enter title of comic to delete it")
        self.bot.register_next_step_handler(message, self.in_database)

    def delete_comics(self, message, value):
        key = [value]
        self.bot.reply_to(message, 'Comics was deleted')
        self.comics_db.delete_comic(key)

    def in_database(self, message):
        key = message.text.lower()
        if self.comics_db.search_comics([key]):
            self.print_comic(message)
            self.bot.reply_to(message, 'Do you want to delete this comic? (yes or no)')
            self.bot.register_next_step_handler(message, self.delete_or_not, key)
        elif key in command_list:
            self.command_choose(message, key)
        else:
            markup = self.menu_keyboard(message)
            self.bot.reply_to(message, "Sorry, I don't find your comic.\n\nIf you want to try againt enter /delete.",
                              reply_markup=markup)

    def delete_or_not(self, message, key):
        value = message.text.lower()
        if value == 'yes':
            self.delete_comics(message, key)
            self.menu_command(message)
        elif value in command_list:
            self.command_choose(message, value)
        elif value == 'no':
            markup = self.menu_keyboard(message)
            self.bot.reply_to(message, "If you want to try againt enter /delete.", reply_markup=markup)
        else:
            markup = self.menu_keyboard(message)
            self.bot.reply_to(message, "I don't recognize your command.\n\nIf you want to try againt enter /delete.",
                              reply_markup=markup)


# delete part end

# print part starts
class print_class:
    def print_command(self, message):
        self.bot.reply_to(message, "Enter title of comics to print it")
        self.bot.register_next_step_handler(message, self.print_in_database)

    def print_info(self, mylist):
        title = f'Title: {mylist[0].upper()}\n'
        chapters = f'Chapters: {mylist[1]}\n'
        author = f'Author: {mylist[2].capitalize()} {mylist[3].capitalize()}\n'
        artist = f'Artist: {mylist[4].capitalize()} {mylist[5].capitalize()}\n'
        kind = f'Kind: {mylist[6].capitalize()}\n'
        genre = f'Genre: {mylist[8].capitalize()}\n'
        periodicity = f'Periodicity: {mylist[9].capitalize()}\n'
        magazine = f'Magazine: {mylist[10].upper()}\n'
        status = f'Status: {mylist[11].capitalize()}\n'
        colorization = f'Colorization: {mylist[12].capitalize()}\n'
        adaptation = f'Adaptation: {mylist[13].capitalize()}\n'
        translation = f'Translation: {mylist[14].upper()} ({mylist[15]})\n'
        return f'{title}{chapters}{author}{artist}{kind}{genre}{periodicity}{magazine}{status}{colorization}{adaptation}{translation}'

    def print_comic(self, message, command=1):
        key = [message.text]
        row = self.comics_db.print_comics(key)
        if command == '/search':
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Save', callback_data='save')
            markup.add(btn1)
            saved.clear()
            saved.append(key)
            user_id.clear()
            user_id.append(message.chat.id)
            print(user_id)
            l = ([x[0] for x in self.comics_db.select_user(user_id)])
            database_id.clear()
            database_id.append(l[0])
            self.bot.reply_to(message, self.print_info(row[0]), disable_notification=True, reply_markup=markup)
        else:
            self.bot.reply_to(message, self.print_info(row[0]))

    def print_in_database(self, message):
        key = message.text.lower()
        if self.comics_db.search_comics([key]):
            self.print_comic(message, '/search')
            self.ask_recommendation(message)
        elif key in command_list:
            self.command_choose(message, key)
        else:
            self.bot.reply_to(message, "Sorry, I don't find your comic.\n\nYou can try to /search again.")
            
    # print part ends
# save part starts
class saved_class:
    def callback_inline(self, call):
        if call.data == 'save':
            re = ([x[0] for x in self.comics_db.print_user(database_id[0])])  # id
            print(re)
            g = str()
            print(type(g))
            g += f'{str(re[0])}'
            print(g)
            save = list()
            save += ([x[0] for x in self.comics_db.search_comics(saved)])
            print(save[0])
            value = str(save[0])
            if value not in g:
                print(value)
                g += f'{str(value)},'
                print(g)
                self.comics_db.update_user(database_id[0], g)  # id
            else:
                pass

    def saved_command(self, message):
        user_id.clear()
        user_id.append(message.chat.id)
        l = ([x[0] for x in self.comics_db.select_user(user_id)])
        database_id.append(l[0])
        save_btn_list = ['menu']
        save_list = ([x[0] for x in self.comics_db.print_user(database_id[0])])  # id
        save_list = save_list[0].split(',')
        save_list.pop()
        save_list = [int(x) for x in save_list]
        if len(save_list) == 0:
            self.bot.reply_to(message, "You haven't saved comics")
        else:
            for i in save_list:
                val = ([x[0] for x in self.comics_db.search_name_by_id(i)])
                save_btn_list.append(val[0])
            markup = self.create_keyboards(save_btn_list)
            self.bot.reply_to(message, "Your saved comics", reply_markup=markup)
            self.bot.register_next_step_handler(message, self.print_saved)

    def print_saved(self, message):
        key = message.text.lower()
        if key in command_list:
            self.command_choose(message, key)
            return
        elif self.comics_db.search_comics([key]):
            self.print_comic(message)
            self.bot.register_next_step_handler(message, self.print_saved)
            return
        elif key == 'menu':
            self.menu_command(message)
            return
        else:
            pass


