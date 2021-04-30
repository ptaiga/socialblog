import asyncio
from collections import defaultdict
from copy import deepcopy


class StorageDriveError(ValueError):
    """Error working with the storage"""
    pass


class Storage:
    """Class for storing metrics"""
    def __init__(self):
        self._data = defaultdict(dict)

    def put(self, metric, value, timestamp):
        self._data[metric][timestamp] = value

    def get(self, metric):
        if metric == '*':
            return deepcopy(self._data)
        if metric in self._data:
            return {metric: deepcopy(self._data[metric])}
        return {}


class StorageDriver:
    """Interface for working with the storage"""
    sep = '\n'
    code_err = 'error'
    code_ok = 'ok'
    error_message = 'wrong command'

    def __init__(self, storage):
        self.storage = storage

    def send_request(self, request):
        try:
            data = self._process_data(request)
            message = ""
            for metric in data:
                for timestamp, value in data.get(metric).items():
                    message += f"{metric} {value} {timestamp}{self.sep}"

            return f"{self.code_ok}{self.sep}{message}{self.sep}"

        except StorageDriveError:
            resp = f"{self.code_err}{self.sep}"
            resp += f"{self.error_message}{self.sep}{self.sep}"
            return resp

    def _process_data(self, data):
        try:
            method, *params = data.split()
        except ValueError:
            raise StorageDriveError

        if method == 'put':
            try:
                metric, value, timestamp = params
                value, timestamp = float(value), int(timestamp)
            except ValueError:
                raise StorageDriveError
            self.storage.put(metric, value, timestamp)
            return {}

        if method == 'get':
            try:
                key = params.pop()
                if params:
                    raise IndexError
            except IndexError:
                raise StorageDriveError
            return self.storage.get(key)

        raise StorageDriveError


class Server(asyncio.Protocol):
    """Class for implementing an asyncio-based server"""
    storage = Storage()
    sep = '\n'

    def __init__(self):
        super().__init__()
        self.driver = StorageDriver(self.storage)
        self._buffer = b''

    def connection_made(self, transport):
        self.transport = transport
        self.addr = self.transport.get_extra_info('peername')
        print(f"Created connection with {self.addr}")

    def data_received(self, data):
        print(f'Received "{data}" from {self.addr}')
        self._buffer += data
        req = self._buffer.decode('utf-8')
        if not req.endswith(self.sep):
            return
        self._buffer = b''
        for line in req.rstrip().splitlines():
            resp = self.driver.send_request(line)
            print(f'Sended "{resp.encode()}" to {self.addr}')
            self.transport.write(resp.encode('utf-8'))


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(Server, host, port)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shut down server")

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server("127.0.0.1", 8765)
