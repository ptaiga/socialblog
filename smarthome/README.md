# Smart Home Project

An example of the interaction between _Smart Home_ systems that supports real-time state configuration. The application is written in _Python_. The following tools are used: _Django_, _SQLite_, _Celery_, _Redis_.

The _Smart Home App_ consists of: 
- `smarthome_server` (_Django_),
- `smarthome_client`:
    - _Web Client_ (_Django_ + _SQLite_),
    - _Task Manager_ (_Celery_ + _Redis_).

The _Server_ provides an _API_ for accessing the data. The _Web Client_ and _Task Manager_ use this _API_ to manage the state of the _Smart Home_.

**This project is intended for use on a local computer and only for familiarization with the proposed code.**


## General logic of interaction

Smart Home has different sensors and devices:

- air_conditioner: true/false,
- bedroom_light: true/false,
- bathroom_light: true/false,
- curtains: "open"/"close"/"slightly_open",
- boiler: true/false,
- cold_water: true/false,
- hot_water: true/false,
- washing_machine: "on"/"off"/"broken",
- bedroom_temperature (read-only): 0-80,
- smoke_detector (read-only): true/false,
- bedroom_presence (read-only): true/false,
- bedroom_motion (read-only): true/false,
- outdoor_light (read-only): 0-100,
- boiler_temperature (read-only): 0-100 / null (if cold_water == false),
- bathroom_presence (read-only): true/false,
- bathroom_motion (read-only): true/false,
- leak_detector (read-only): true/false

Management (read/write) is performed via the _Server_ using specific _API_ at http://127.0.0.1:8001/server/.

The format of the _JSON_ response to the request (_GET_ and _POST_):
```
{"status": "ok", "data": [{"name": "boiler", "value": "true"}, {...}, ...]}
```

The device values are recorded by sending _JSON_ data via a _POST_ request:
```
{"controllers": [{"name": "boiler", "value": "true"}, {...}, ...]}
```


## Requirements

Before launching the _Smart Home_ components, you need to create a working virtual environment and install the following necessary dependencies:
```
python==3.6
requests==2.18.4
celery==4.1.1
django==2.0
redis==2.10.6
```

Before doing this, make sure that you have _Redis_ (https://redis.io/topics/quickstart) installed on local machine.

Also, in a virtual environment, it is important to set:
```
DJANGO_SECRET_KEY
```

and preferably set the following variables:
```
EMAIL_HOST
EMAIL_PORT
EMAIL_RECEPIENT
EMAIL_TIMEOUT
EMAIL_USE_SSL
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```


## Server

To start the _Server_, open the console, go to the `smarthome_server` folder and run the command: 
```
python manage.py runserver 8001
```
After that, access to the _Server_ will be at http://127.0.0.1:8001/server/.

The _Server_ is a simple layer between the requests from _Web Client_ and _Task Manager_ on the one hand and the data that is stored in the file `data.json` on the other. This file can be __edited manually and thus emulate the changes__ that occur with sensors and devices of _Smart Home_.

For example, you can activate the `leak_detector`. As a result of the next request to the _Server_, the _Task Manager_ will see this and turn off the water, boiler, washing machine, and also send an email about the leak detection. For details of the algorithm conditions, see below.


## Web Client

To start the _Web Client_, open the console, go to the `smarthome_client` folder and at the first start roll out the migrations to the database.
```
python manage.py migrate
```
Thne run the command: 
```
python manage.py runserver
```

After that, the client application will be available at http://127.0.0.1:8000.

On the client page, you can see the current values of all sensors and devices, as well as set the values of the following parameters:

- bedroom_target_temperature: 16-50,
- bathroom_target_temperature: 24-90,
- bedroom_light: true/false,
- bathroom_light: true/false.


## Task Manager

To activate the _Task Manager_ (in _Unix_ systems), run the following command in the console in the `smarthome_client` folder.
```
celery -A smarthome_client.celery worker -l info -B
```

For the _Windows_ operating system, due to poor _Celery_ support, you need to run two commands in two different consoles. One command starts a _worker_ to handle _periodic tasks_. The second one creates and sends _periodic tasks_ to the _worker_.
```
celery -A smarthome_client.celery worker --pool=solo -l info
celery -A smarthome_client.celery beat -l info
```

_Celery_ uses _Redis_ as a broker.

_Task Manager_ configures the devices by accessing the server via the _API_ every 10 seconds, taking into account the following conditions:

- If there is a water leak (`leak_detector=true`), close the cold (`cold_water=false`) and hot (`hot_water=false`) water and send an email at the time of detection.

- If the cold water (`cold_water`) is closed, immediately turn off the boiler (`boiler`) and the washing machine (`washing_machine`) and under no circumstances turn them on until the cold water is opened again.

- If the hot water has a temperature (`boiler_temperature`) less than `hot_water_target_temperature - 10%`, it is necessary to turn on the boiler (`boiler`), and wait until it reaches the temperature `hot_water_target_temperature + 10%`, after which, in order to save energy, the boiler must be turned off.

- If the curtains are partially open (`curtains="slightly_open"`), then they are manually operated - this means that their state cannot be changed automatically under any circumstances.

- If the street (`outdoor_light`) is darker than _50_, open the curtains (`curtains`), but only if the lamp in the bedroom is not lit (`bedroom_light`). If the street (`outdoor_light`) is lighter than _50_, or the light is on in the bedroom (`bedroom_light`), close the curtains. Except when they are manually operated.

- If smoke is detected (`smoke_detector`), immediately turn off the following devices: `air_conditioner`, `bedroom_light`, `bathroom_light`, `boiler`, `washing_machine` - and under no circumstances turn them on until the smoke disappears.

- If the temperature in the bedroom (`bedroom_temperature`) has risen above `bedroom_target_temperature + 10%` - turn on the air conditioner (`air_conditioner`), and wait until the temperature drops below `bedroom_target_temperature - 10%`, then turn off the air conditioner.
