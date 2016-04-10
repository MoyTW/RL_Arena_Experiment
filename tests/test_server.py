import unittest
import requests
import threading
import hunting.server as server


class TestRunEndpoint(unittest.TestCase):
    def setUp(self):
        self.port = server.get_random_open_port()
        self.server = server.new_server(self.port)

        def start_on_port():
            self.server.serve_forever()
        server_thread = threading.Thread(target=start_on_port)
        server_thread.start()

    def tearDown(self):
        self.server.shutdown()

    def url(self, path):
        url = 'http://localhost:{0}/{1}'.format(self.port, path)
        return url

    def test_run_codes(self):
        # 200 if valid
        r200 = requests.get(self.url('run/test/hero_versus_zero.json'))
        self.assertEqual(r200.status_code, 200)

        # 404 if invalid resource
        r404 = requests.get(self.url('run/test/whatwhattheheck.idontknow'))
        self.assertEqual(r404.status_code, 404)

        # 500 if bad json
        r500 = requests.get(self.url('run/test/deformed.json'))
        self.assertEqual(r500.status_code, 500)
