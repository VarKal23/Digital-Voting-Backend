## Digital Voting Backend
A voting api and database that mimics a Democratic Party Election. Created with FastAPI, PostgreSQL, and Python.

## Project Status
- Adding more integration tests/fixing old ones
- Fixing CI/CD Pipeline, workflows bugging
- Need to deploy to Netlify instead of Heroku (Heroku no longer free)
- Adding more features to the existing routes

## Installation and Setup Instructions
Clone down this repository:
`git clone https://github.com/VarKal23/Digital-Voting-Backend.git`

Navigate to the root directory of the project:
`cd digital-voting-backend`

Create a virtual environment:
`python -m venv venv` or however is required by your system

Activate your virtual environment:
`venv\Scripts\activate.ps1` for Windows Powershell (use correct script for terminal)

Install the required dependencies:
`pip install -r requirements.txt`

Run the server:
`uvicorn app.main:app`

Create a PostgreSQL database and add a .env file with the following in the root of the project directory
- DATABASE_HOSTNAME=
- DATABASE_PORT=
- DATABASE_PASSWORD=
- DATABASE_NAME=
- DATABASE_USERNAME=
- SECRET_KEY=
- ALGORITHM=
- ACCESS_TOKEN_EXPIRE_MINUTES=

Go to the docs to test routes:
- Click on the url that appears in the terminal
- Once you see the "Hello World" message, add a "/docs" to the url and you will see an autocreated FastAPI interface page for testing the routes

## Reflection
This was a project I wanted to develop because I've felt that as technology has become more reliable, the possibility of online voting for Democratic elections like the presidential race would streamline the entire process. Especially in the aftermath of Covid and mail-in ballots becoming more common, I feel that an online voting system would be much more reliable and efficient. Obviously there are a lot of security concerns that I don't address in my application, but I hope that one day these issues can be fixed and a platform like mine can be used for elections.

This project was challenging because this was my deep dive into backend development as well as dipping my toes in DevOps. I was learning a lot of the tools along the way and testing them in many different ways to try to get this application to work. The DevOps aspects are still a work in progress but the core functionality of my application is there.

The technologies I used were FastAPI, PostgreSQL, SQLAlchemy, PyTest, Postman, Docker, and Github Actions. FastAPI was a convenient way to build this API and provided the docs feature to provide some nice documentation and interface. PostgreSQL was used because of the structured queries and relational data sets I needed to make/have and I used SQLAlchemy as the ORM to connect my Python code to the database instead of writing actual SQL to query the database. PyTest was used for easy integration testing as it provided nice feedback with a clean interface and Postman was used to test the API as I went. Docker and Github Actions were used for DevOps purposes as they were the most convenient and popular choices and I wanted to take a crack at and learn these tools.
