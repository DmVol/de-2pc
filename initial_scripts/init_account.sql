CREATE TABLE accounts (
	Account_ID serial PRIMARY KEY,
	Client_Name VARCHAR (50) NOT NULL,
	Amount INT NOT NULL CHECK(Amount >= 0)
);

INSERT INTO accounts (Client_Name, Amount) VALUES 
('John Snow', 200),
('Walter White', 950)