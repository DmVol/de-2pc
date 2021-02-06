CREATE TABLE hotel_booking (
	Booking_Id serial PRIMARY KEY,
	Client_Name VARCHAR (50) NOT NULL,
	Hotel_Name VARCHAR (50) NOT NULL,
	Arrival DATE NOT NULL ,
	Departure DATE NOT NULL
);