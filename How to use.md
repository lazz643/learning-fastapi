# Welcome to proyek fast api

ini adalah proyek pembelajaran crud fastapi

## How to run Backend

- Go to phpmyadmin and create the same name database like the name of database in .env file
  ![alt text](image.png)

- Make migration database model file with:
  => alembic revision --autogenerate -m "create users table"

- Launch the migration file with:
  => alembic upgrade head

- Run the backend server with:
  => uvicorn app.main:app --reload

## How to run Frontend

- Go to phpmyadmin and create the same name database like the name of database in .env file

- Make migration database model file with:
  => alembic revision --autogenerate -m "create users table"

- Launch the migration file with:
  => alembic upgrade head

- Run the backend server with:
  => uvicorn app.main:app --reload
