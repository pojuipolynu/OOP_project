import mysql.connector
import math


class Comic:

    def __init__(self, set_host, set_name, set_password, set_database):
        self.mydb = mysql.connector.connect(
            host=set_host,
            user=set_name,
            password=set_password,
            database=set_database
        )

    def search_author(self, search):
        mycursor = self.mydb.cursor()
        sql = "SELECT idauthor FROM author WHERE surname = %s;"
        mycursor.execute(sql, search)
        myresult = mycursor.fetchall()
        return myresult

    def search_artist(self, search):
        mycursor = self.mydb.cursor()
        sql = "SELECT idartist FROM artist WHERE surname = %s;"
        mycursor.execute(sql, search)
        myresult = mycursor.fetchall()

        return myresult

    def search_genre(self, search):
        mycursor = self.mydb.cursor()
        sql = "SELECT idgenre FROM genre WHERE name = %s;"
        mycursor.execute(sql, search)
        myresult = mycursor.fetchall()
        return myresult

    def search_translation(self, search, leg):
        mycursor = self.mydb.cursor()
        if leg == 'official':
            sql = "SELECT idtranslation FROM translation WHERE language = %s AND legality = 'official';"
        elif leg == 'non-official':
            sql = "SELECT idtranslation FROM translation WHERE language = %s AND legality = 'non-official';"
        else:
            raise TypeError
        mycursor.execute(sql, search)
        myresult = mycursor.fetchall()
        return myresult

    def search_magazine(self, search):
        mycursor = self.mydb.cursor()
        sql = "SELECT idmagazine FROM magazine WHERE title = %s;"
        mycursor.execute(sql, search)
        myresult = mycursor.fetchall()
        return myresult

    def insert_author(self, name, surname):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO author (surname, name) VALUES (%s, %s)"
        val = list(surname)
        val.append(name)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def insert_artist(self, name, surname):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO artist (surname, name) VALUES (%s, %s)"
        val = list(surname)
        val.append(name)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def insert_genre(self, title):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO genre (name, subgenre) VALUES (%s, %s)"
        val = title + title
        mycursor.execute(sql, val)
        self.mydb.commit()

    def insert_translation(self, title, title1, id):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO translation (language, legality, status_idstatus) VALUES (%s, %s, %s)"
        val = list()
        val.append(title)
        val.append(title1)
        val += ([x[0] for x in id])
        mycursor.execute(sql, val)
        self.mydb.commit()

    def insert_magazine(self, title, num, id):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO magazine (title, number, periodicity_idperiodicity) VALUES (%s, %s, %s)"
        val = list()
        val += title
        val.append(num)
        val += ([x[0] for x in id])
        mycursor.execute(sql, val)
        self.mydb.commit()

    def select_name(self, key):
        if not isinstance(key, str):
            raise TypeError
        return key

    def select_num(self, key):
        return key

    def select_period(self, key, keyl):
        mycursor = self.mydb.cursor()
        if key not in ['every day', 'every week', 'every month', 'non-periodical']:
            return False
        else:
            sql = "SELECT idperiodicity FROM periodicity WHERE period = %s;"
            mycursor.execute(sql, keyl)
            l = mycursor.fetchall()
            return l

    def select_status(self, key, keyl):
        mycursor = self.mydb.cursor()
        if key not in ['frozen', 'ongoing', 'completed']:
            return False
        else:
            sql = "SELECT idstatus FROM status WHERE name = %s;"
            mycursor.execute(sql, keyl)
            l = mycursor.fetchall()
            return l

    def select_color(self, key, keyl):
        mycursor = self.mydb.cursor()
        if key not in ['monochrome', 'non-monochrome', 'lineart']:
            return False
        else:
            sql = "SELECT idcolourization FROM colourization WHERE name = %s;"
            mycursor.execute(sql, keyl)
            l = mycursor.fetchall()
            return l

    def select_kind(self, key, keyl):
        mycursor = self.mydb.cursor()
        if key not in ['manga', 'manhwa', 'manhua', 'comics', 'maliopys']:
            return False
        else:
            sql = "SELECT idkind FROM kind WHERE name = %s;"
            mycursor.execute(sql, keyl)
            l = mycursor.fetchall()
            return l

    def select_adapt(self, key, keyl):
        mycursor = self.mydb.cursor()
        if key not in ['film', 'cartoon', 'tvshow', 'show', 'anime']:
            return False
        else:
            sql = "SELECT idadaptation FROM adaptation WHERE type = %s;"
            mycursor.execute(sql, keyl)
            l = mycursor.fetchall()
            return l

    def insert_comics(self, key, choice, l):
        keyl = list()
        keyl.append(key)
        if choice == 'title':
            l['name'] = self.select_name(key)
        elif choice == 'genre':
            if self.search_genre(keyl):
                l[choice] = ([x[0] for x in (self.search_genre(keyl))])
            else:
                self.insert_genre(keyl)
                l[choice] = ([x[0] for x in (self.search_genre(keyl))])
        elif choice == 'author':
            if self.search_author(keyl):
                l[choice] = ([x[0] for x in (self.search_author(keyl))])
            else:
                self.insert_author(input('It seems that your author is not in our database.'
                                         'Please help us by entering his name!\n'), keyl)
                l[choice] = ([x[0] for x in (self.search_author(keyl))])
        elif choice == 'artist':
            if self.search_artist(keyl):
                l[choice] = ([x[0] for x in (self.search_artist(keyl))])
            else:
                self.insert_artist(input('It seems that your artist is not in our database.'
                                         'Please help us by entering his name!\n'), keyl)
                l[choice] = ([x[0] for x in (self.search_artist(keyl))])
        elif choice == 'periodicity':
            l[choice] = ([x[0] for x in (self.select_period(key, keyl))])
        elif choice == 'magazine':
            if self.search_magazine(keyl):
                l[choice] = ([x[0] for x in (self.search_magazine(keyl))])
            else:
                o = input('It seems that your magazine is not in our database. Please help us by entering its '
                          'circulation!\n')
                e = input('Thank you! Also enter, please, its periodicity!\n')
                se = list()
                se.append(e)
                self.insert_magazine(keyl, o, self.select_period(e, se))
                l[choice] = ([x[0] for x in (self.search_magazine(keyl))])
        elif choice == 'chapters':
            l[choice] = self.select_num(int(key))
        elif choice == 'status':
            l[choice] = ([x[0] for x in (self.select_status(key, keyl))])
        elif choice == 'colorization':
            l[choice] = ([x[0] for x in (self.select_color(key, keyl))])
        elif choice == 'kind':
            l[choice] = ([x[0] for x in (self.select_kind(key, keyl))])
        elif choice == 'adaptation':
            l[choice] = ([x[0] for x in (self.select_adapt(key, keyl))])
        elif choice == 'translation':
            #leg = input('Is your translation official or non-official?\n')
            if self.search_translation(keyl, 'official'):
                l[choice] = ([x[0] for x in (self.search_translation(keyl, 'official'))])
            else:
                e = input('Also enter, please, what`s your translation status!\n')
                se = list()
                se.append(e)
                self.insert_translation(key, 'official', self.select_status(e, se))
                l[choice] = ([x[0] for x in (self.search_translation(keyl, 'official'))])
        else:
            raise TypeError
        return l

    

    def insert_all(self, l):
        comiclist1 = []
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO comics (name, genre_idgenre, author_idauthor, artist_idartist, periodicity_idperiodicity," \
              "magazine_idmagazine, num_chapter, status_idstatus, colourization_idcolourization, kind_idkind," \
              "adaptation_idadaptation, translation_idtranslation) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        comiclist = [l['name'], l['genre'], l['author'], l['artist'], l['periodicity'], l['magazine'],
                     l['chapters'], l['status'], l['colorization'], l['kind'], l['adaptation'], l['translation']]
        for x in comiclist:
            if isinstance(x, list):
                comiclist1 += x
            else:
                comiclist1.append(x)
        mycursor.execute(sql, comiclist1)
        self.mydb.commit()

    def print_comics(self, name):
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM comics WHERE name = %s;"
        mycursor.execute(sql, name)
        myresult = mycursor.fetchall()
        return myresult
    
    #delete part starts
        def search_comics(self, search):
        mycursor = self.mydb.cursor()
        sql = "SELECT idcomics FROM comics WHERE name = %s;"
        mycursor.execute(sql, search)
        myresult = mycursor.fetchall()
        return myresult

    def delete_comic(self, name):
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM comics WHERE idcomics = %s;"
        val = self.search_comics(name)
        vall = list()
        vall += ([x[0] for x in val])
        mycursor.execute(sql, vall)
        self.mydb.commit()
        
    #delete part ends

