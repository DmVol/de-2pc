from faker import Faker
import psycopg2
import random
from psycopg2._psycopg import DatabaseError

connection_accounts = psycopg2.connect("dbname='my_db' user='test' host='localhost' password='test' " "port='5434'")
connection_flights = psycopg2.connect("dbname='my_db' user='test' host='localhost' password='test' " "port='5432'")
connection_hotels = psycopg2.connect("dbname='my_db' user='test' host='localhost' password='test' " "port='5433'")
# create Faker generator
fake = Faker()
# Define a dictionary of the top 20 busiest airports in the world (in 2018)
airports = {"ATL": "Hartsfield–Jackson Atlanta International Airport",
            "PEK": "Beijing Capital International Airport",
            "DXB": "Dubai International Airport",
            "LAX": "Los Angeles International Airport",
            "HND": "Tokyo Haneda Airport",
            "ORD": "O'Hare International Airport (Chicago)",
            "LHR": "London Heathrow Airport",
            "SAR": "Hong Kong International Airport",
            "PVG": "Shanghai Pudong International Airport",
            "CDG": "Paris-Charles de Gaulle Airport",
            "AMS": "Amsterdam Airport Schiphol",
            "DEL": "Indira Gandhi International Airport (Delhi)",
            "CAN": "Guangzhou Baiyun International Airport",
            "FRA": "Frankfurt Airport",
            "DFW": "Dallas/Fort Worth International Airport",
            "ICN": "Seoul Incheon International Airport",
            "IST": "Istanbul Atatürk Airport",
            "CGK": "Soekarno-Hatta International Airport",
            "SIN": "Singapore Changi Airport",
            "DEN": "Denver International Airport",
            }


def check_user(user_name):
    cursor_user = connection_accounts.cursor()
    cursor_user.execute(f"SELECT * FROM accounts WHERE client_name = '{user_name}';")
    connection_accounts.commit()
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
        # Begin transactions
        connection_accounts.tpc_begin(connection_accounts.xid(42, '1', 'connection_account'))
        connection_flights.tpc_begin(connection_flights.xid(42, '2', 'connection_flights'))
        connection_hotels.tpc_begin(connection_hotels.xid(42, '3', 'connection_hotels'))
        # Create cursors
        cursor_flights = connection_flights.cursor()
        cursor_hotels = connection_hotels.cursor()
        cursor_accounts = connection_accounts.cursor()
        # Create fake dates
        start_date = fake.date_between(start_date='today', end_date='+30d')
        end_date = fake.date_between(start_date=start_date, end_date='+30d')
        # Execute needed commands
        cursor_hotels.execute("""INSERT INTO hotel_booking (Client_Name, Hotel_Name, Arrival, Departure)
                                 VALUES (%s, %s, %s, %s);""", (user_name, fake.company(), start_date, end_date))
        cursor_flights.execute("""INSERT INTO fly_booking (Client_Name, Fly_Number, Fly_From, Fly_To, Fly_Date)
                                   VALUES (%s, %s, %s, %s, %s);""",
                               (user_name, fake.license_plate(), random.choice(list(airports.keys())),
                                random.choice(list(airports.keys())), start_date))
        cursor_accounts.execute(
            f"UPDATE accounts SET Amount = Amount - {random.randint(50, 250)} WHERE client_name = '{user_name}';")
        connection_accounts.tpc_prepare()
        connection_flights.tpc_prepare()
        connection_hotels.tpc_prepare()
    except DatabaseError:
        print("Rollback transactions")
        connection_accounts.tpc_rollback()
        connection_flights.tpc_rollback()
        connection_hotels.tpc_rollback()
    else:
        print("Commit transactions")
        connection_accounts.tpc_commit()
        connection_flights.tpc_commit()
        connection_hotels.tpc_commit()


if __name__ == "__main__":
    inp = input("Specify user name: ")
    data = check_user(inp)
    if data:
        booking(data)
