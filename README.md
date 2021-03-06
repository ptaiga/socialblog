# Examples of code

This repository contains code examples of projects written using **_Python_** and other related technologies: *Django*, *HTML*, *CSS*, *SQLite*, *PostgreSQL*, *Redis*, *Celery*, *Git*. Here is just a brief description of each project. For more information, go to the appropriate folder.

**Note**. If the project contains a `projectname-git.zip`-archive (the full contents of the project and `.git`-folder), you can download and unzip it. As a result you will get the files and commit history of this project.

- [`/socialblog`](https://github.com/ptaiga/examples/tree/master/socialblog) &mdash; Test task for creating a blog platform with social media capabilities. The version is implemented using _Python_ and _Django_.

- [`/geotelebot`](https://github.com/ptaiga/examples/tree/master/geotelebot) &mdash; Prototype of a working _Telegram Bot_. Helps the user to save and view interesting places (name, address, geo-position and photo). When sending a location, it shows which of these places are within a 500-meter radius. The project is written in _Python_, prepared for rolling out to _Heroku_-hosting, and uses _PostgreSQL_ to save data.

- [`/smarthome`](https://github.com/ptaiga/examples/tree/master/smarthome) &mdash; An example of the interaction between _Smart Home_ systems that supports real-time state configuration. The application is written in _Python_. The following tools are used: _Django_, _SQLite_, _Celery_, _Redis_.

- [`/cipher`](https://github.com/ptaiga/examples/tree/master/cipher) &mdash; Implementation of the _Caesar_ cipher and its two variations _Rot13_ and _Vigenere_. The performance of each of the ciphers is checked by using unit testing.

- [`/somemart`](https://github.com/ptaiga/examples/tree/master/somemart) &mdash; Realization of a simple API for an online store: add a product, add a review to the product, get a product description and all reviews for it. All actions are performed via _GET_ or _POST_ requests using _JSON_. Unauthorized users can get a product description or add a review to the product. Admin's rights allow to add new products. User authentication is performed via [_HTTP Basic Auth_](https://en.wikipedia.org/wiki/Basic_access_authentication). Data validation is performed using `django.forms`, `jsonschema` and `marshmallow`. The project is made using _Django_. For testing used `pytest`.

- [`/herokuapp`](https://github.com/ptaiga/examples/tree/master/herokuapp) &mdash; Step-by-step guide to creating a simple web application that shows the number of page views in _Python_ and _Django_ using _Redis_. It also shows how to roll out the application to _Heroku_ hosting using _Git_.

- [`/gameoflife`](https://github.com/ptaiga/examples/tree/master/gameoflife) &mdash; Console utility for demonstrating the famous _"Conway's Game of Life"_. The implementation is made using the __Python__ language and _OOP_ principles.

- [`/asyncsocket`](https://github.com/ptaiga/examples/tree/master/asyncsocket) &mdash; A system for collecting and storing metrics based on a client-server architecture. Examples of such systems are _Graphite_ and _InfluxDB_. The clients and server communicate with each other over a simple text protocol via _TCP-sockets_. To implement an asynchronous server, use the following popular _Python_-libriry: __asyncio__. To implement a clients, use the other popular _Python_-libriry: _socket_.
