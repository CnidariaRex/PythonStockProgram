__author__ = 'Rex'


import ystockquote
import sqlite3
import time
import sys
import os


def main():

    conn = sqlite3.connect('test.db')


    if conn:
        print("Opened database successfully")

        if conn.execute('drop table if exists STOCKS'):
            print('Successfully dropped table')

        conn.execute('create table STOCKS (ID int PRIMARY KEY, NAME text, PRICE float, CHANGE float, PERCENT float, RATIO float)')


    tickersymbols = ['EA', 'CSX', 'SPY', 'ADSK', 'AAPL', 'MSFT', 'GE', 'DXJ', 'ZNGA', 'GPRO', 'GOOG']

    for tickerSymbol in tickersymbols:

        name = tickerSymbol

        position = tickersymbols.index(name)

        allInfo = ystockquote.get_all(tickerSymbol)

        price = float(allInfo["price"])

        change = float(allInfo["change"])

        percent = change/(change + price)*100

        peratio = allInfo["price_earnings_ratio"]

        conn.execute('insert into STOCKS(ID,NAME,PRICE,CHANGE,PERCENT,RATIO) VALUES(?, ?, ?, ?, ?, ?)', (position, tickerSymbol, price, change, percent, peratio))

    if conn.commit():
        print("Records created successfully")

    while True:
        try:
            for tickerSymbol in tickersymbols:

                string_name = tickerSymbol

                allInfo = ystockquote.get_all(tickerSymbol)

                price = float(allInfo["price"])

                change = float(allInfo["change"])

                percent = change/(change + price)*100

                peratio = allInfo["price_earnings_ratio"]

                conn.execute("UPDATE STOCKS set PRICE = ?, CHANGE = ?, PERCENT = ?, RATIO = ? where NAME = ?", (price, change, percent, peratio, tickerSymbol))

            if conn.commit():
                print("Records created successfully")

            cursor = conn.execute("SELECT ID, NAME, PRICE, CHANGE, PERCENT, RATIO  from STOCKS")
            for row in cursor:
                print("ID = ", row[0], "/ NAME = ", row[1], "/ PRICE = ", row[2], "/ CHANGE = ", row[3], "/ PERCENT = ", row[4], "/ RATIO = ", row[5], "\n")
            time.sleep(10)
        except:
            print("Error updating database")

if __name__ == '__main__':
    try:
        print("Starting program")
        main()
    except KeyboardInterrupt:
        print("Interupted")
        try:
            sys.exit(0)
        except:
            os.exit(0)