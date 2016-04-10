import unittest
import requests
import threading
import json
import hunting.server as server
import hunting.resources as resources


def sort_dicts(obj):
    if isinstance(obj, dict):
        return sorted((k, sort_dicts(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return (sort_dicts(x) for x in obj)
    else:
        return obj


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

    def test_run_contents_simple(self):
        response = requests.get(self.url('run/test/hero_versus_zero.json'))
        parsed_response = sort_dicts(response.json())
        with open(resources.get_full_path('test/results/hero_versus_zero.json')) as f:
            expected = sort_dicts(json.load(f))
        self.assertEqual(parsed_response, expected)
