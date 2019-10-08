from datetime import date
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error


def lotto_scraping(website="https://www.lotto.pl/"):
    """Web scraping to get a str with a number"""
    page_html = urlopen(website)
    soup = BeautifulSoup(page_html, "html.parser")
    content = soup.find_all("div", {"class": "number text-center"})

    fetched_lotto = ""
    fetched_lotto_plus = ""

    for div in content[:6]:
        number = div.text.strip()
        fetched_lotto += number + "-"

    for div in content[6:12]:
        number = div.text.strip()
        fetched_lotto_plus += number + "-"

    pack = (fetched_lotto[:-1], fetched_lotto_plus[:-1])

    return pack


class DataMingler:

    @staticmethod
    def connector(db_file="lotto.db"):
        cnx = None

        try:
            cnx = sqlite3.connect(db_file)
        except Error as e:
            print("CNX problem in DataMingler.connector:", e)

        return cnx

    def button_add_to_db(self, my_number):
        sql_query = "INSERT INTO my_numbers(my_num, date) VALUES(?, ?)"
        today = date.today().strftime("%Y-%m-%d")
        params = (my_number, today)
        cnx = self.connector()
        cursor = cnx.cursor()

        try:
            cursor.execute(sql_query, params)
        except Error as e:
            print("Cursor problem in DataMingler.button_to_add:", e)
        finally:
            cursor.close()
            cnx.commit()
            cnx.close()

    def numbers_comparison(self):
        sql_query = "SELECT my_num FROM my_numbers"
        cnx = self.connector()
        cursor = cnx.cursor()

        winner = None
        loosers = []
        try:
            cursor.execute(sql_query)
            data = cursor.fetchall()
            fetched_lotto = lotto_scraping()[0]
            fetched_lotto_plus = lotto_scraping()[1]

            for row in data:
                for n in row:
                    if n == fetched_lotto or n == fetched_lotto_plus:
                        winner = row
                    else:
                        loosers.append(row)

        except Error as e:
            print("Cursor problem in DataMingler.button_to_add:", e)
        finally:
            cursor.close()
            cnx.close()

        text_win = ""
        text_lose = ""

        if winner:
            if winner[0]:
                text_win = f"Your number {winner[0]} wins!"
            else:
                text_win = "None of your numbers win."

        if len(loosers) == 0:
            text_lose = "No numbers to check!"
        elif len(loosers) == 1:
            text_lose = f"Your number {loosers[0][0]} did not win this time."
        elif len(loosers) > 1:
            text_lose = "None of your numbers below wins.\n"
            for tup in loosers:
                for el in tup:
                    text_lose += f"{el}\n"

        pack = (text_win, text_lose)
        return pack

    def add_current_number(self):
        insert_query = "INSERT INTO previous_numbers(prev_number, date) VALUES(?, ?), (?, ?)"

        fetched_lotto = lotto_scraping()[0]
        fetched_lotto_plus = lotto_scraping()[1]

        today = date.today().strftime("%Y-%m-%d")
        params = (fetched_lotto, today, fetched_lotto_plus, today)

        cnx = self.connector()
        cursor = cnx.cursor()

        try:
            cursor.execute(insert_query, params)
        except Error as e:
            print(e, "<-- If this exception is about UNIQUE constraint, do not worry and enjoy your lotto! :)")
        finally:
            cursor.close()
            cnx.commit()
            cnx.close()

    def show_old_numbers(self):
        sql_query = "SELECT prev_number FROM previous_numbers"
        cnx = self.connector()
        cursor = cnx.cursor()

        try:
            cursor.execute(sql_query)
            cursor_data = cursor.fetchall()
        except Exception as e:
            print("Cursor problem in DataMingler.show_old_numbers:", e)
        finally:
            cursor.close()
            cnx.close()

        if cursor_data:
            return cursor_data

        return "Something went terribly wrong, my friend..."
