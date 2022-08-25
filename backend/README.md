# Backend server

This project uses FastAPI. To read the docs: https://fastapi.tiangolo.com/
First install all dependencies:

```bash
pip install -r requirements.txt
```

To start webserver:

```bash
uvicorn main:app --reload
```


**IMPORTANT**: when starting the webserver, Instagram might prompt with 2-FA token request. You should enter the token using the CLI in order for the app to properly work.

