# AsyncSocket

A system for collecting and storing metrics based on a client-server architecture. Examples of such systems are _Graphite_ and _InfluxDB_. The clients and server communicate with each other over a simple text protocol via _TCP-sockets_. To implement an asynchronous server, use the following popular _Python_-libriry: __asyncio__. To implement a clients, use the other popular _Python_-libriry: _socket_.

The examples below will collect data about the operation of the operating system of several servers. This will allow to monitor and control the server load, as well as make forecasts for the expansion of the hardware fleet.


## Interaction protocol

The protocol supports two types of requests to the server from the client side:
- sending data to save it on the server,
- getting saved data.


### General format of the client request
```
<command> <request data><\n>
```

- &lt;command&gt; &ndash; can take one of two values:
    - `put` &ndash; save the data on the server;
    - `get` &ndash; return saved data form the server.

- &lt;request data&gt; &ndash; format of the request data will be described in more detail in the examples below.

- &lt;\n&gt; &ndash; line break character indicates the end of the command.


### General format of the server response
```
<status><\n><response data><\n\n>
```

- &lt;status&gt; &ndash; there are two possible options for the command execution status:
    - `ok` &ndash; command completed successfully;
    - `error` &ndash; command execution failed.

- &lt;response data&gt; &ndash; optional field (the format of the response data and the cases of its absence will be described in the examples below), separated from &lt;status&gt; by &lt;\n&gt;

- &lt;\n\n&gt; &ndash; two line break characters indicate the end of the response.


### Examples of client-server interaction


#### PUT

PUT-request for saving data will be constructed as follows:

```
put <key> <value> <timestamp>\n
```

- &lt;key&gt; (&lt;server&gt;.&lt;metric&gt;) &ndash; can consist of two parts: the name of the server and the metric that we save. We can save usage of CPU, RAM, hard disk, network, etc. For example, `serv.cpu` or `vers.memory`.

- &lt;value&gt; &ndash; value of metric in floating-point number format.

- &lt;timestamp&gt; &ndash; time measurement is accurate to the second. If the metric value with this time is already saved, it will be overwritten with the new value.

For example, on 'April 26, 2021 16:55:20' for server 'serv' CPU usage was '42.3%':
```
put serv.cpu 42.3 1619445320\n
```

If the data is saved successfully, the server response will be:
```
ok\n\n
```

If an error occurs, the server will respond:
```
error\nwrong command\n\n
```


#### GET

To get information about the saved data, you need to send a GET-request like:
```
get <key>\n
```

- &lt;key&gt; &ndash; the following variations are possible:
    - `*` &ndash; to get all saved data for every metric;
    - &lt;server&gt;.&lt;metric&gt; &ndash; to get all saved data for specific metric.

For example:
```
get serv.cpu\n
```

If the data is available, the server will respond:
```
ok\nserv.cpu 42.3 1619445320\n\n
```

If there is no data for the specified metric, for example, when you request `get vers.memory\n`, the server will respond:
```
ok\n\n
```


#### More examples

Assume that the following data is stored on the server:

 key          | value | timestamp  
--------------|-------|------------
"serv.cpu"    |  42.3 | 1619445320
"serv.cpu"    |  2.0  | 1619445380
"vers.memory" |  1024 | 1619445400

```
# Request (overwrites the existing data in the second row):
put serv.cpu 4.0 1619445380\n

# Response:
ok\n\n
```
```
# Request (wrong data in request):
put serv.cpu\n

# Response:
error\nwrong command\n\n
```
```
# Request (get all saved data):
get *\n

# Response:
ok\nserv.cpu 42.3 1619445320\nserv.cpu 4.0 1619445380\nvers.memory 1024 1619445400\n\n
```
```
# Request (get data for specific metric):
get vers.memory\n

# Response:
ok\nvers.memory 1024 1619445400\n\n
```
```
# Request (metric is non-exist):
get serv.memory\n

# Response:
ok\n\n
```


## Client


### Description

The client implementetion is located in file `client.py`.

Class `Client` encapsulates a connection to the server, a client socket, and methods for getting (`get`) and sending (`put`) metrics to the server.

When creating an instance of the `Client`, the address pair host and port and the optional timeout parameter are passed to the constructor. At this point, the connection to the server is created and is not interrupted until the work is completed.


### Method `put`

Method `put` takes name of the metric, numeric value and the optional parameter timestamp. If the user called the `put` method without the timestamp, the client should automatically substitute the current time value.

Method returns nothing if the data is sent successfully and throws a custom `ClientError` exception if it is not successful.


### Method `get`

Method `get` takes as a parameter the name of the metric or '\*'-symbol, which was mentioned in the protocol description.

Method returns a dictionary with metrics (see the example below) if the response from the server is successful, and throws a `ClientError` exception if it is not successful.

The client receives data from the server in text form, the method `get` process the response string and return the dictionary with the received keys from the server. The value of the keys in the dictionary is a list of tuples:
```
[(timestamp1, value1), (timestamp2, value2), …]
```

The `timestamp` and `value` are converted to the `int` and `float` types, respectively. The list of values is sorted by the `timestamp` in ascending order.

If the server returns a positive `ok\n\n` response to the `get` request without any data (i.e. there is no data for the requested key), the client's `get` method should return an empty dictionary `{}`.


### Example

```
>>> from client import Client
>>> client = Client("127.0.0.1", 8765, timeout=15)
>>> client.put("serv.cpu", 42.3, timestamp=1619445320)
>>> client.put("serv.cpu", 2.0, timestamp=1619445380)
>>> client.put("serv.cpu", 4.0, timestamp=1619445380)
>>> client.put("vers.memory", 1024, timestamp=1619445400)
>>> client.put("vers.memory", 2048, timestamp=1619445460)
>>> client.put("vers.cpu", 100)
>>> print(client.get("*"))
{
  'serv.cpu': [
    (1619445320, 42.3),
    (1619445380, 4.0)
  ],
  'vers.memory': [
    (1619445400, 1024.0),
    (1619445460, 2048.0)
  ],
  'vers.cpu': [
    (1619445432, 100.0)
  ]
}
```

Note that the server stores data with a maximum resolution of one second. This means that if two identical metrics are sent at the same second, only last value will be saved. All other values will be overwritten. For this reason, the request for the key "serv.cpu" returned data only from two dimensions.


### Testing

The code for testing the `Client` class is located in the file `test_client.py` and is run by the command:
```
$ python -m unittest test_client.py
```


## Server


### Description

The server implementation enforces the protocol for communicating with clients that is described above. The server receives `put` and `get` commands from clients, parses them, and generates a response according to the protocol. When working with the clients, the server supports sessions, that is, the connection with the client is not broken between requests.

The server starts with the command:
```
$ python server.py 
```

By default listens for incoming connections to the host `127.0.0.1` and port `8765`.

When a `put`-request is received, the passed metrics are stored in a special data structure in the process memory.

When a `get`-request is received, the server sends the requested data in the correct sequence.


### Using `asyncio`

As the basis for the implementation, a simple TCP-server on `asyncio` is used.
```
import asyncio


class Server(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


loop = asyncio.get_event_loop()
coro = loop.create_server(Server, '127.0.0.1', 8765)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
```

This code creates a TCP-connection for the address `127.0.0.1:8765` and listens for all incoming requests. When the client is connected, a new instance of the class `Server` is created, and when new data is received, the `data_received` method of this object is called. Inside `asyncio.Protocol` hides all the magic of processing requests through coroutines.

This server can handle requests from multiple clients at the same time.


### Implementation

The server implementation for receiving metrics is located in the file `server.py`.

The application code is divided into classes: `Server`, `Storage`, `StorageDriver` and `StorageDriveError`.

- `Server` &ndash; class that implements an asyncio-server, the basic example for which is given above.

- `Storage` &ndash; encapsulates methods for working with the storage. In this case, the metrics are simply stored in a dictionary in memory, but the class is easy to expand and add, for example, persistence and other properties.

- `StorageDriver` &ndash; class that represents the interface for working with the storage. Passing the storage object during initialization allows to abstract from the specific implementation of the storage itself (data can be stored on the file system or on a remote server, while the class `StorageDriver` will provide the necessary interface).

- `StorageDriverError` &ndash; exception that is thrown when an error occurs in parsing and processing the received data. This exception is caught to ensure the stability of the server.

The `Server` accepts and buffers the data. Then it passes them to the `StorageDriver`, where the data is parsed, processed, and the necessary actions are performed with the `Storage`.

This division of the application logic into several classes makes it easy to modify the program and add new functionality. It is also much easier to perceive and debug code that performs a specific task than code that does everything at once.


### Example

You can connect to the server using the client described above, or, for example, using _Telnet_ (console utility). This is what the text protocol will look like in action when using the _Telnet_:
```
$: telnet 127.0.0.1 8765
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
> get test_key
< ok
< 
> got test_key
< error
< wrong command
< 
> put test_key 12.0 1503319740
< ok
< 
> put test_key 13.0 1503319739
< ok
< 
> get test_key 
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< 
> put another_key 10 1503319739
< ok
< 
> get *
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739
< 
```

### Testing

For local testing of the server, the script `test_server.py` is created, which uses the client implementation from the file `client.py`. 

The server starts in the first console:
```
python server.py
```

To run the tests, executed the command in other console:
```
python test_server.py
```
