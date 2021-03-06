import sqlite3
import time, os

filename = "scrapper_db"
db = None
try:
    
    #there will therefore alsobe a separate table for storing the scripts extracted from a table, yet to be classified as malicious
    #create/connect to the database
    def connect():
        create = not os.path.exists(filename)
        db = sqlite3.connect(filename)
        if create:
            cursor = db.cursor()

            cursor.execute("CREATE TABLE url_scan ("
                           "scan_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                           "url TEXT NOT NULL, "
                           "scan_date TEXT NOT NULL, "
                           "current_hash TEXT NOT NULL,"
                           "initial_hash TEXT )")

            cursor.execute("CREATE TABLE js_string ("
                           "string_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,"
                           "string TEXT NOT NULL,"
                           "regex TEXT ,"
                           "effect_of_js TEXT NOT NULL)")

            cursor.execute("CREATE TABLE scan_report ("
                           "report_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                           "url TEXT NOT NULL, "
                           "XSS_result TEXT NOT NULL ,"
                           "scan_date DATETIME NOT NULL)")

            cursor.execute("CREATE TABLE positive_scan ("
                           "positive_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                           "scan_id INTEGER NOT NULL,"
                           "url TEXT NOT NULL,"
                           "string TEXT NOT NULL,"
                           "other_js_string TEXT NOT NULL,"
                           "code_index TEXT NOT NULL,"
                           "effect_of_js TEXT NOT NULL,"
                           "remedy TEXT NOT NULL)")
            db.commit()
        return db

    def insert_scan(url, scan_date, current_hash, initial_hash):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("INSERT INTO url_scan "
                       "(url, scan_date, current_hash, initial_hash)"
                       "VALUES (?, ?, ?, ?)", (url, scan_date, current_hash, initial_hash))
        db.commit()

    def insert_js_string(string, regex, effect_of_js):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("INSERT INTO js_string "
                       "(string, regex, effect_of_js)"
                       "VALUES (?, ?, ?)", (string, regex, effect_of_js))
        db.commit()

    def insert_scan_report(url, xss_result, scan_date):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("INSERT INTO scan_report "
                       "(url, xss_result, scan_date)"
                       "VALUES (?, ?, ?)", (url, xss_result, scan_date))
        db.commit()

    def insert_positive_scan(scan_id, url, string, other_js, current_code_index, effect_of_js, remedy):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("INSERT INTO positive_scan "
                       "(scan_id, url, string, other_js_string, code_index, effect_of_js, remedy)"
                       "VALUES (?, ?, ?, ?, ?, ?, ?)", (int(scan_id), str(url), string, other_js, current_code_index, effect_of_js, remedy,))
        db.commit()

    def get_js_string(regex):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT string FROM js_string WHERE regex = ?", (regex,))
        fields = cursor.fetchone()
        return fields[0] if fields is not None else None

    def get_effect_of_js(regex):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT effect_of_js FROM js_string WHERE regex = ?", (regex,))
        fields = cursor.fetchone()
        return fields[0] if fields is not None else None

    def get_url(url):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT scan_id FROM url_scan WHERE url = ?", (url,))
        fields = cursor.fetchone()
        return 1 if fields is not None else None

    def get_initial_hash(url):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT initial_hash FROM url_scan WHERE url = ? ORDER BY scan_id DESC", (url,))
        fields = cursor.fetchone()
        return fields[0] if fields is not None else None

    def get_scan_id(url):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT scan_id FROM url_scan WHERE url = ? ORDER BY scan_id DESC", (url,))
        fields = cursor.fetchone()
        return fields[0] if fields is not None else None

    def get_negative_scan_report(url):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM scan_report WHERE url = ? ORDER BY report_id  DESC", (url,))
        fields = cursor.fetchone()
        return fields if fields is not None else None
    
    def get_positive_scan_report(url):
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM positive_scan WHERE url = ? ORDER BY positive_id DESC", (url, ))
        fields = cursor.fetchone()
        return fields if fields is not None else None

    def get_payloads():
        connect()
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT regex FROM js_string")
        fields = cursor.fetchall()
        return fields if fields is not None else None 
        

finally:
    if db is not None:
        db.close()
