import time
import socket


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        try:
            self.sock = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError("Cannot open socket", err)

    def _send(self, data):
        # self.sock.settimeout(5)
        try:
            self.sock.sendall(data)
        except socket.error as err:
            raise ClientError("Error sending data to socket", err)

    def _read(self):
        data = b""
        # self.sock.settimeout(5)
        while not data.endswith(b"\n\n"):
            try:
                data += self.sock.recv(1024)
            except socket.error as err:
                raise ClientError("Error reading data from socket", err)
        return data

    def get(self, metric):
        self._send(f"get {metric}\n".encode("utf-8"))
        response = self._read().decode("utf-8").strip().splitlines()
        print(response)
        status, payload = response[0], response[1:]
        data = {}
        if status != "ok":
            raise ClientError("Server returns an error")

        for line in payload:
            metric, value, timestamp = line.split()
            if metric not in data:
                data[metric] = []
            data[metric].append((int(timestamp), float(value)))
            {data[key].sort() for key in data}

        return data

    def put(self, metric, value, timestamp=int(time.time())):
        self._send(f"put {metric} {value} {timestamp}\n".encode("utf-8"))
        if self._read() != b"ok\n\n":
            raise ClientError("Server returns an error")

    def close(self):
        try:
            self.sock.close()
        except socket.error as err:
            return ClientError("Cannot close socket", err)


def main():
    wait = 1
    client = Client("127.0.0.1", 8765, timeout=15)
    client.put("serv.cpu", 42.3, timestamp=1619445320)
    time.sleep(wait)
    client.put("serv.cpu", 2.0, timestamp=1619445380)
    time.sleep(wait)
    client.put("serv.cpu", 4.0, timestamp=1619445380)
    time.sleep(wait)
    client.put("vers.memory", 1024, timestamp=1619445400)
    time.sleep(wait)
    client.put("vers.memory", 2048, timestamp=1619445460)
    time.sleep(wait)
    client.put("vers.cpu", 100)
    time.sleep(wait)
    print(client.get("*"))
    client.close()


if __name__ == '__main__':
    main()
