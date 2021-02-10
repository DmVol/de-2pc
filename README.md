# Data engineering - Two Phase Commit
Implementation of two-phase commit protocol
# Implementation
- PostgreSQL databases were used for accounts, hotels & flight booking
- Hosted databases as Docker containers
- Coordinator is written on Python using psycopg2 library for DB connection
# Creating DB instances:
docker-compose up --build

DDL and DML statements will be executed as a part of instance creation
# Running the app:
Execute 2pc_coordinator.py file to run the application

NOTE: Only predefined users (John Snow, Walter White) will be avaliable for input
