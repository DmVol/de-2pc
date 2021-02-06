import datetime

from faker import Faker
import psycopg2
import random

from psycopg2._psycopg import DatabaseError

connection_account = psycopg2.connect("dbname='my_db' user='test' host='localhost' password='test' "
                                      "port='5434'")
connection_flights = psycopg2.connect("dbname='my_db' user='test' host='localhost' password='test' "
                                      "port='5432'")
connection_hotels = psycopg2.connect("dbname='my_db' user='test' host='localhost' password='test' "
                                     "port='5433'")


def check_user(user_name):
    cursor_user = connection_account.cursor()
    cursor_user.execute(f"SELECT * FROM accounts WHERE client_name = '{user_name}';")
    connection_account.commit()
    user_data = cursor_user.fetchone()
    cursor_user.close()
    if user_data:
        print(user_data)
        return user_data
    else:
        print("No such user")

def booking(user_data):
    user_name = user_data[1]
    try:
        xid1 = connection_account.xid(42, '1', 'connection_account')
        connection_account.tpc_begin(xid1)
        connection_flights.tpc_begin(connection_flights.xid(42, '2', 'connection_flights'))
        connection_hotels.tpc_begin(connection_hotels.xid(42, '3', 'connection_hotels'))
        cursor_flights = connection_flights.cursor()
        cursor_hotels = connection_hotels.cursor()
        cursor_accounts = connection_account.cursor()
        cursor_hotels.execute("""INSERT INTO hotel_booking (Client_Name, Hotel_Name, Arrival, Departure)
                                 VALUES (%s, %s, %s, %s);""",
                              (user_name, "Hilton", datetime.date(2005, 11, 18), datetime.date(2005, 12, 18)))
        cursor_flights.execute("""INSERT INTO fly_booking (Client_Name, Fly_Number, Fly_From, Fly_To, Fly_Date)
                                   VALUES (%s, %s, %s, %s, %s);""",
                               (user_name, "AHV31", "LVV", "IVF", datetime.date(2005, 11, 18)))
        cursor_accounts.execute(f"UPDATE accounts SET Amount = Amount - {random.randint(50, 250)} WHERE client_name = '{user_name}';")
        connection_account.tpc_prepare()
        connection_flights.tpc_prepare()
        connection_hotels.tpc_prepare()
    except DatabaseError:
        connection_account.tpc_rollback()
        connection_flights.tpc_rollback()
        connection_hotels.tpc_rollback()
    else:
        connection_account.tpc_commit()
        connection_flights.tpc_commit()
        connection_hotels.tpc_commit()

inp = input("Specify user name: ")

data = check_user(inp)
if data:
    booking(data)
