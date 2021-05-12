# Astro-BE

## Setup

Setup instructions can be found [on notion](https://www.notion.so/Local-Development-Setup-028ca15eddf44a24923ab982cee53d1c).

## Scripts

### Export the current packages

To export the current package requirements to the requirements file, run:

```shell
pip freeze > requirements.txt
```

### Start the server

To start the server, run:

```shell
uvicorn main:app --reload
```

This will start the server running locally at `http://127.0.0.1:8000`.

### View the API documentation

Once the server is running, you can view the API documentation at `http://127.0.0.1:8000/docs`, 
or on linux by running:

```shell
xdg-open http://127.0.0.1:8000/docs
```