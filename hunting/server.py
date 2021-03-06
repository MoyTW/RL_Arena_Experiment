import http.server
import threading
import socket

import tdl
import hunting.level.parser as parser
import hunting.level.encoder as encoder
from hunting.display.render import Renderer
import hunting.sim.runner as runner
import hunting.resources as resources


UTF_8 = 'utf-8'


def get_random_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def shutdown_server_from_new_thread(server):
    def kill_server():
        server.shutdown()

    killer = threading.Thread(target=kill_server)
    killer.start()


class HelloWorldHandler(http.server.BaseHTTPRequestHandler):
    def hello_world(self):
        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()

        payload = bytes('Hello World!', UTF_8)
        self.wfile.write(payload)

    def goodbye(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(bytes('Shutting down!\n', UTF_8))
        shutdown_server_from_new_thread(self.server)

    def what(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(bytes("I don't know what that is!", UTF_8))

    def test_vis(self, file_path):
        full_path = resources.get_full_path(file_path)
        level = parser.parse_level(full_path)
        runner.run_level(level)

        main_console = tdl.init(level.width, level.height, 'TDL Test')

        scratch_level = parser.parse_level(full_path)
        renderer = Renderer(main_console, level.width, level.height)
        renderer.render_all(level=scratch_level)

        for event in level.log.events:
            renderer.render_event(level=scratch_level, event=event)

        main_console.__del__()  # Crude, but this whole thing is crude.

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(encoder.encode_level(level), UTF_8))

    def run_file(self, file_path):
        full_path = resources.get_full_path(file_path)
        if full_path is not None:
            try:
                level = parser.parse_level(full_path)
                runner.run_level(level)

                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()

                self.wfile.write(bytes(encoder.encode_level(level), UTF_8))

            except ValueError as err:
                self.send_response(500)
                self.send_header('content-type', 'text/plain')
                self.end_headers()

                self.wfile.write(bytes('Error: {0}'.format(err), UTF_8))
        else:
            self.send_response(404)
            self.send_header('content-type', 'text/plain')
            self.end_headers()

            self.wfile.write(bytes('No such file!', UTF_8))


    def do_GET(self):
        if self.path == '/goodbye':
            self.goodbye()
        elif self.path == '/hello':
            self.hello_world()
        elif self.path.startswith('/test_vis/'):
            self.test_vis(self.path[10:])
        elif self.path.startswith('/run/'):
            self.run_file(self.path[5:])
        else:
            self.what()


def new_server(port):
    return http.server.HTTPServer(("", port), HelloWorldHandler)


def start_server(port=8888):
    print('starting on port', port)
    httpd = new_server(port)
    httpd.serve_forever()
    print('server shut down')
