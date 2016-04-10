import http.server
import threading


def shutdown_server_from_new_thread(server):
    def kill_server():
        server.shutdown()

    killer = threading.Thread(target=kill_server)
    killer.start()


class HelloWorldHandler(http.server.BaseHTTPRequestHandler):
    def hello_world(self):
        self.send_response(200)
        self.wfile.write(bytes('Hello World!', 'utf-8'))

    def goodbye(self):
        self.send_response(200)
        self.wfile.write(bytes('Shutting down!\n', 'utf-8'))
        self.end_headers()
        shutdown_server_from_new_thread(self.server)

    def do_GET(self):
        if self.path == '/goodbye':
            self.goodbye()
        else:
            self.hello_world()


def start_server(port=8888):
    print('starting on port', port)
    httpd = http.server.HTTPServer(("", port), HelloWorldHandler)
    httpd.serve_forever()
    print('server shut down')
