# This is your main script.

try:
    import usocket as socket
except:
    import socket

import ure
import ujson

REQUEST_REGEX = r"^(\S+)\s+(\S+)\s+(\S+)\\r\\n.*$"


def send_400(connection):
    connection.send('HTTP/1.1 400 Not\n')
    connection.send('Connection: close\n\n')


def socket_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8040))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = str(conn.recv(256))
        res = ure.match(REQUEST_REGEX, request)
        if not res:
            print("Unhandled request: ", request)
            send_400(conn)
            continue

        if res.group(2) == '/temp':
            resp_data = {
                'bme_temperature': float(bme.temperature.strip('C')),
                'bme_humidity': float(bme.humidity.strip('%')),
                'bme_pressure': float(bme.pressure.strip('hPa')),
            }

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: application/json\n')
            conn.send('Connection: close\n\n')
            conn.sendall(ujson.dumps(resp_data))
        else:
            print("Unhandled request: ", request)
            send_400(conn)
        conn.close()


if __name__ == "__main__":
    socket_server()