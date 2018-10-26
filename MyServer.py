import socket
import threading
import queue
import web
import errors
import CustomScriptLanguageV2
import datetime

host = "127.0.0.1"
port = 9000

connection = socket.socket()
connection.bind((host, port))
connection.listen(5)


def find_html_file(path):
    try:
        if path == "/":
            with open('index.html', 'r') as f:
                html_file = f.read()
                html_parsed = CustomScriptLanguageV2.parse_html_custom(html_file)
        else:
            with open(path[1:], 'r') as f:
                html_file = f.read()
                html_parsed = CustomScriptLanguageV2.parse_html_custom(html_file)
        response_status = "200"
        response_status_text = "OK"
        return html_parsed, response_status, response_status_text
    except FileNotFoundError:
        with open("errors/404.html", 'r') as f:
            html = f.read()
            response_status = "404"
            response_status_text = 'Not Found'
            return html, response_status, response_status_text


def send_html(path, conn):
    html_to_browser, response_status, response_status_text = find_html_file(path)

    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(html_to_browser),  # msg
        # 'Connection': 'close',
    }

    response_headers_raw = ''.join('{}: {}\r\n'.format(k, v) for k, v in response_headers.items())

    response_proto = 'HTTP/1.1'

    # sending all this stuff
    r = '{}{}{}\r\n'.format(response_proto, response_status, response_status_text)
    conn.send(r.encode(encoding="utf-8"))
    conn.send(response_headers_raw.encode(encoding="utf-8"))
    conn.send('\r\n'.encode(encoding="utf-8"))  # to separate headers from body
    conn.send(html_to_browser.encode(encoding="utf-8"))  # msg.


def accept_connections():
    while True:
        # conn, addr = connection.accept()
        # t1 = threading.Thread(target=parse_request, args=(conn,))
        # t1.start()
        conn, addr = connection.accept()
        request_queue = queue.Queue()  # Thread safe
        request_queue.put(conn)
        if request_queue.qsize() <= 5:
            t1 = threading.Thread(target=parse_request, args=(conn,))  # tuple because of conn, not a tuple if only conn
            t1.start()
            request_queue.get()


def parse_request(conn):
    http_request = conn.recv(1024).decode()

    header, rest = http_request.split('\r\n', 1)
    print("header:", header) #contains request type and path
    print("rest:", rest)

    request_type, path, rest2 = header.split(' ')
    print("path is:", path)
    if path != "/favicon.ico":
        # Log http request
        logfile = open("request_logfile.txt", "a")
        logfile.write(header + "Time: " + str(datetime.datetime.now()) + "\n")

        if request_type == "GET":
            try:
                send_html(path, conn)
            except:
                print("General error!")
    conn.close()


accept_connections()