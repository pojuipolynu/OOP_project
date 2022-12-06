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
        val.append(title[0])
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
        sql = "SELECT idperiodicity FROM periodicity WHERE period = %s;"
        mycursor.execute(sql, keyl)
        l = mycursor.fetchall()
        return l

    def select_status(self, key, keyl):
        mycursor = self.mydb.cursor()
        sql = "SELECT idstatus FROM status WHERE name = %s;"
        mycursor.execute(sql, keyl)
        l = mycursor.fetchall()
        return l

    def select_color(self, key, keyl):
        mycursor = self.mydb.cursor()
        sql = "SELECT idcolourization FROM colourization WHERE name = %s;"
        mycursor.execute(sql, keyl)
        l = mycursor.fetchall()
        return l

    def select_kind(self, key, keyl):
        mycursor = self.mydb.cursor()
        sql = "SELECT idkind FROM kind WHERE name = %s;"
        mycursor.execute(sql, keyl)
        l = mycursor.fetchall()
        return l

    def select_adapt(self, key, keyl):
        mycursor = self.mydb.cursor()
        sql = "SELECT idadaptation FROM adaptation WHERE type = %s;"
        mycursor.execute(sql, keyl)
        l = mycursor.fetchall()
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


    #delete part

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

    def print_comics(self, name):
        mycursor = self.mydb.cursor()
        sql = "SELECT\
              comics.name AS ncomic,\
              comics.num_chapter AS chapter,\
              author.name AS nauthor,\
              author.surname AS sauthor,\
              artist.name AS nartist,\
              artist.surname AS sartist,\
              kind.name AS kname,\
              genre.subgenre AS subgenre,\
              genre.name AS gname,\
              periodicity.period AS pperiod,\
              magazine.title AS mtitle,\
              status.name AS sname,\
              colourization.name AS cname,\
              adaptation.type AS atype,\
              translation.language AS tlanguage,\
              translation.legality AS tlegality\
              FROM comics\
              INNER JOIN genre ON comics.genre_idgenre = genre.idgenre\
              INNER JOIN author ON comics.author_idauthor = author.idauthor\
              INNER JOIN artist ON comics.artist_idartist = artist.idartist\
              INNER JOIN periodicity ON comics.periodicity_idperiodicity = periodicity.idperiodicity\
              INNER JOIN magazine ON comics.magazine_idmagazine = magazine.idmagazine\
              INNER JOIN status ON comics.status_idstatus = status.idstatus\
              INNER JOIN colourization ON comics.colourization_idcolourization = colourization.idcolourization\
              INNER JOIN kind ON comics.kind_idkind = kind.idkind\
              INNER JOIN adaptation ON comics.adaptation_idadaptation = adaptation.idadaptation\
              INNER JOIN translation ON comics.translation_idtranslation = translation.idtranslation\
              WHERE idcomics = %s;"
        val = self.search_comics(name)
        vall = list()
        vall += ([x[0] for x in val])
        mycursor.execute(sql, vall)
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

    def update_genre(self, key, key1):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET genre_idgenre = %s WHERE idcomics = %s;"
        val = self.search_genre(key)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key1])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_author(self, key, key1):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET author_idauthor = %s WHERE idcomics = %s;"
        val = self.search_author(key)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key1])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_artist(self, key, key1):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET artist_idartist = %s WHERE idcomics = %s;"
        val = self.search_artist(key)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key1])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_period(self, key, key1, key2):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET periodicity_idperiodicity = %s WHERE idcomics = %s;"
        val = self.select_period(key, key1)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key2])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_magazine(self, key, key1):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET magazine_idmagazine = %s WHERE idcomics = %s;"
        val = self.search_magazine(key)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key1])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_status(self, key, key1, key2):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET status_idstatus = %s WHERE idcomics = %s;"
        val = self.select_status(key, key1)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key2])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_color(self, key, key1, key2):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET colourization_idcolourization = %s WHERE idcomics = %s;"
        val = self.select_color(key, key1)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key2])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_kind(self, key, key1, key2):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET kind_idkind = %s WHERE idcomics = %s;"
        val = self.select_kind(key, key1)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key2])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_adapt(self, key, key1, key2):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET adaptation_idadaptation = %s WHERE idcomics = %s;"
        val = self.select_adapt(key, key1)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key2])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_trans(self, key, key1, leg):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET translation_idtranslation = %s WHERE idcomics = %s;"
        val = self.search_translation(key, leg)
        vall = list()
        vall += ([x[0] for x in val])
        vall += ([x[0] for x in key1])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_name(self, key, key1):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET name = %s WHERE idcomics = %s;"
        vall = list()
        vall.append(key)
        vall += ([x[0] for x in key1])
        mycursor.execute(sql, vall)
        self.mydb.commit()

    def update_num(self, key, key1):
        mycursor = self.mydb.cursor()
        sql = "UPDATE comics SET num_chapter = %s WHERE idcomics = %s;"
        vall = list()
        vall.append(key)
        vall += ([x[0] for x in key1])
        mycursor.execute(sql, vall)
        self.mydb.commit()

