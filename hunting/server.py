import http.server
import threading

import tdl
import hunting.level.parser as parser
import hunting.level.encoder as encoder
from hunting.display.render import Renderer
import hunting.sim.runner as runner


UTF_8 = 'utf-8'


def shutdown_server_from_new_thread(server):
    def kill_server():
        server.shutdown()

    killer = threading.Thread(target=kill_server)
    killer.start()


class HelloWorldHandler(http.server.BaseHTTPRequestHandler):
    def hello_world(self):
        self.send_response(200)
        self.wfile.write(bytes('Hello World!', UTF_8))

    def goodbye(self):
        self.send_response(200)
        self.wfile.write(bytes('Shutting down!\n', UTF_8))
        shutdown_server_from_new_thread(self.server)

    def what(self):
        self.send_response(200)
        self.wfile.write(bytes("I don't know what that is!", UTF_8))

    def test_json(self):
        level = parser.parse_level('resources/test_level.json')
        runner.run_level(level)

        self.send_response(200)
        self.wfile.write(bytes(level.log.to_json_string()))

    def test_vis(self):
        level = parser.parse_level('resources/test_level.json')
        runner.run_level(level)

        main_width = 80
        main_height = 60
        level_width = 80
        level_height = 50

        main_console = tdl.init(main_width, main_height, 'TDL Test')

        scratch_level = parser.parse_level('resources/test_level.json')
        renderer = Renderer(main_console, level_width, level_height)
        renderer.render_all(level=scratch_level)

        for event in level.log.events:
            renderer.render_event(level=scratch_level, event=event)

        main_console.__del__()  # Crude, but this whole thing is crude.

        self.send_response(200)
        self.wfile.write(bytes(encoder.encode_level(level), UTF_8))

    def do_GET(self):
        if self.path == '/goodbye':
            self.goodbye()
        elif self.path == '/hello':
            self.hello_world()
        elif self.path == '/test_json':
            self.test_json()
        elif self.path == '/test_vis':
            self.test_vis()
        else:
            self.what()


def start_server(port=8888):
    print('starting on port', port)
    httpd = http.server.HTTPServer(("", port), HelloWorldHandler)
    httpd.serve_forever()
    print('server shut down')
