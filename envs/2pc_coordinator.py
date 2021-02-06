from faker import Faker
import psycopg2

conn = psycopg2.connect("dbname='my_db' user='test' host='localhost' password='test' "
                        "port='5434'")
cur = conn.cursor()
cur.execute("SELECT * FROM accounts;")
one = cur.fetchone()

print(one)