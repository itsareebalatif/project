# Week 3(Day 1)


## What I Use:

* FASTAPI: for handling the API endpoints and auto-docs.
* SQLAlchemy: + SQLite for talking to the database.
* Pydantic v2: for validating incoming request data (like emails and passwords).
* Passlib (bcrypt): for securely encrypting passwords 
* JWT: for keeping users logged in securely.-->Tokens
* Loggers: so you can see when users sign up or log in right in your console.

---

## How to runn this:

First, clone or download the repo, then open up your terminal in the project folder and follow these steps:

## Create and activate a VE:

   python3 -m venv venv
   source venv/bin/activate
   and at the end run : ./venv/bin/python -m uvicorn app.main:app --reload