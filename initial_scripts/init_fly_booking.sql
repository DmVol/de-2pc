CREATE TABLE fly_booking (
	Booking_Id serial PRIMARY KEY,
	Client_Name VARCHAR (50) NOT NULL,
	Fly_Number VARCHAR (50) NOT NULL,
	Fly_From VARCHAR (3) NOT NULL,
	Fly_To VARCHAR (3) NOT NULL,
	Fly_Date DATE NOT NULL 
);