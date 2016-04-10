import sys
import http.server
import threading
import socketserver
import uuid

import tdl

import hunting.level.parser as parser
import hunting.level.encoder as encoder
from hunting.display.render import Renderer
from hunting.sim.runner import run_level

#main_width = 80
#main_height = 60
#level_width = 80
#level_height = 50

#main_console = tdl.init(main_width, main_height, 'TDL Test')

#level = parser.parse_level('resources/test_level.json')

#run_level(level)

#print(level.log.to_json_string())

# This is not very elegant, but the level used for doing the calculations is destructive, so we need to get a fresh
# from-json copy for rendering.
#scratch_level = parser.parse_level('resources/test_level.json')

#renderer = Renderer(main_console, level_width, level_height)
#renderer.render_all(level=scratch_level)

#for event in level.log.events:
#    renderer.render_event(level=scratch_level, event=event)

#print(encoder.encode_level(level))

PORT = 8888


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


Handler = HelloWorldHandler

httpd = http.server.HTTPServer(("", PORT), Handler)

print('starting on port', PORT)
httpd.serve_forever()
print('server shut down')
