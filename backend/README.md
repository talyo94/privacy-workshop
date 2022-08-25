# Backend server

This project uses FastAPI. To read the docs: https://fastapi.tiangolo.com/
First install all dependencies:

```bash
pip install -r requirements.txt
```


Setup env variables:

Copy the `.env.example` file to `internal/.env` and fill the values.
Those are required values to authenticate with Instgram and store data on backend (redis).


To start webserver:

```bash
uvicorn main:app --reload
```


**IMPORTANT**: when starting the webserver, Instagram might prompt with 2-FA token request. You should enter the token using the CLI in order for the app to properly work.

