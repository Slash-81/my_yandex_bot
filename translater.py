import requests
import json
import sys
import sqlite3
import os


API_KEY = "trnsl.1.1.20190811T194659Z.3b434556e2cdc7e1.8f32164ff88b838e0794881eef8cc40ea878035c"
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"

class Translator():

    def __init__(self, *args, **kwargs):

        self.text = input("Print text>>")
        self.lang = input("Print language fot translate>>")
        self.url = "{0}?key={1}&text={2}&lang={3}".format(URL, API_KEY, self.text, self.lang)

        #self.url = "{0}?key={1}&{2}".format(URL, API_KEY,f"text={kwargs['text']}&lang={kwargs['lang']}")

    def get_answer(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.result = response.json()
        else:
            self.result = {}

    def vew_answer(self):
        template = f"""Перевод с/на {self.result["lang"]} языка такой:
        {self.result["text"]}"""
        print(template)

def create_db(path):
    if not os.path.isfile(path):
        with open(path, 'wb') as file:
            pass
    return

def get_connect(path):
    connect = sqlite3.connect(path)
    return connect

def create_table(connect):
    sql = """CREATE TABLE IF NOT EXISTS "Translation" (
            "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "lang"	TEXT UNIQUE,
            "word"	TEXT,
        );"""
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()

def get_data(object):
    data = json.dumps(object)

    return data

def send_answer(element, connect):
    sql = f"""INSERT INTO "Translation" (
            "lang",
            "word"
    )
    VALUE (
        "{element['lang']}",
        "{element['word']}"
    );
    """
    cursor = connect.cursor()
    cursor.execute(sql)

if __name__ == '__main__':

    obj = Translator()
    #print(obj.url)
    obj.get_answer()
    obj.vew_answer()

    if len(sys.argv) > 2:
        path = os.path.join(sys.argv[1], sys.argv[2])
        create_db(path)
        connection = get_connect(path)
        create_table(connection)
        send_answer(obj.result, connection)

    else:
        print("Wrong args")