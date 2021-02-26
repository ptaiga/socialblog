# Geolocation Telegram Bot

Prototype of a working _Telegram Bot_. Helps the user to save and view interesting places (name, address, geo-position and photo). When sending a location, it shows which of these places are within a 500-meter radius. The project is written in _Python_, prepared for rolling out to _Heroku_-hosting, and uses _PostgreSQL_ to save data.

## Usage

This bot will help you save interesting places and show you which ones are nearby.

You can use commands (into _Telegram_):
- `/add` - New location item. _"/add name and address"_ - quick addition or _"/add"_ for step-by-step  dialog.
- `/list` - List of 10 last location items.
- `/more` - Show detailed information about last location item.
- `/location` - Locations within 500 meters radius. _"/location x,y"_ or attach location.
- `/reset` - Delete all saved location items.


## Guide

The _Bot_ can be run locally or rolled out to a remote hosting (for example, [_Heroku_](https://www.heroku.com/)). Data (including photos) is stored using _PostgreSQL_ or locally (in-memory and files).

### Dependencies

To run the project, the following dependencies must be installed in the virtual environment together with `python3`: 

- `pytelegrambotapi` &ndash; module [_pyTelegramBotAPI_](https://github.com/eternnoir/pyTelegramBotAPI) simplifies working with the [_Telegram Bot API_](https://core.telegram.org/bots/api).

- `psycopg2-binary` &ndash; module [_Psycopg_](https://www.psycopg.org/docs/usage.html) is necessary for working with the _PostgreSQL_.

### Variables

- `TOKEN` &ndash; Required to authorize the bot and send requests to the [_Bot API_](https://core.telegram.org/bots/api).
- `DATABASE_URL` &ndash; If the path to the database is not specified, the location data will be stored in memory, and the photo will be stored in a folder on disk.
- `ADMIN_ID`  &ndash; The _Telegram ID_ of the user who will receive the logs of requests to the _Bot_.

[Here](https://core.telegram.org/bots#6-botfather) is a description of how to get `TOKEN` for the _Bot_. This is done through [`@BotFather`](https://t.me/botfather), the one bot that rule all the others. It will help create new bots and change settings for existing ones.

The `TOKEN` for the bot must be set as an environment variable. Locally, for example, in the console, before launching the bot, you need to write: `$ set TOKEN={token-value}`. In the case of remote hosting, for example, [_Heroku_](https://www.heroku.com/), this is done in the settings of your personal account in the _"Config Vars"_ section.

### Launch

#### Locally

To begin with, you can run `python test.py` to simply check that the _Bot_ accepts data and responds. In this test, the _Bot_ waits for a photo to be sent to it, saves it to a disk in folder `/photo`, and sends it back to the user.

If everything went fine, then you can run the main module `python main.py`.

#### Heroku

We will look deploy using _Heroku Git_ (use _Git_ in the command line or a _GUI_ tool to deploy this app), but there are other ways. 

On the [_Dashboard_](https://dashboard.heroku.com/apps), you need to:
- create an _App_, 
- add a _Heroku Postgre_ to it, 
- and set _Confid Vars_. 

All other actions are performed on the local computer. 

You must install the following applications on local machine, if they are not already installed:

- [_Git_](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [_Heroku CLI_](https://devcenter.heroku.com/articles/heroku-command-line)

Next, on the local machine, we connect to _Heroku_, initialize the repository (if suddenly it does not exist yet) and specify the application on _Heroku_ as the remote repository.
```
$ heroku login
$ git init
$ heroku git:remote -a your-app-name
```

The deployment process is that we send local changes to a remote repository.
```
$ git add .
$ git commit -m "Initial commit"
$ git push heroku master
```

_Heroku_ finds the file `requirement.txt` and sets the specified dependencies.

To launch the application, you need `Procfile` that specifies what the hosting should run. The file contains command for worker `worker: python main.py`. In the console, you need to run:
```
$ heroku ps:scale worker=1
```

To stop it you need to perform: `$ heroku ps:scale worker=0`

This is all you need to launch the _Bot_. At the same time, __the free features of *Heroke* will be enough and you will not have to pay__.


## Files

The text above already mentions the files and their purpose: `test.py`, `requirements.txt`, `Procfile`. Here we will take a closer look at the rest of the project files/modules.

- `main.py` &ndash; The main file where all the logic of the _Bot_ is implemented.

- `storage.py` &ndash; The module is responsible for storing user data.

- `point.py` &ndash; A small auxiliary module that stores the coordinates of locations as objects of the class and provides the coordinates in a convenient form for PostgreSQL.

- `distance.py` &ndash; Calculation of distances between points on the Earth's surface according to the _Haversine formula_.
