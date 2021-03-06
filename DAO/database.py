import os
import sqlite3
from pathlib import Path


class DatabaseConn:

    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(str(Path(os.getcwd()).parent)+"\\"+"auth.db")
        except sqlite3.Error as e:
            print(e)

    def create_table(self):
        try:
            c = self.conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS Authentication ( user text PRIMARY KEY, pass text)')
            self.conn.commit()
        except sqlite3.Error as error:
            print("Error while creating table", error)

    def create_user(self, username, password):
        try:
            c = self.conn.cursor()
            with self.conn:
                c.execute("INSERT INTO Authentication VALUES(?, ?)", (username, password))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return 'User already exists'
        finally:
            c.close()

    def get_user_by_name_and_pass(self, name, pwd):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Authentication WHERE user = ? AND pass = ?", (name, pwd))
        return c.fetchall()

    def get_user_by_name(self, name):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Authentication WHERE user = :user", {'user': name})
        return c.fetchall()

    def fetch_users_all(self):
        c = self.conn.cursor()
        c.execute("SELECT user FROM Authentication")
        return c.fetchall()

    def remove_user(self, name):
        c = self.conn.cursor()
        c.execute("DELETE  FROM Authentication WHERE user = :user ", {'user': name} )
        self.conn.commit()

    def drop_table(self, conn):
        c = conn.cursor()
        c.execute("DROP TABLE Authentication")
