__author__ = 'oleh'

import Main
import mock
import unittest
from functions import generate_array


class DotsTest(unittest.TestCase):
    def test_generate_array(self):
        self.assertEqual(generate_array(0), [], "CHECK generate array")
        self.assertNotEqual(generate_array(2), [], "CHECK generate array")

    @mock.patch('Main.server')
    def test_server(self, mock_server):
        mock_server.return_value = "Hello, I'm server"
        self.assertEqual(Main.server(), "Hello, I'm server", "Server doesn't respond")

    @mock.patch('Main.worker')
    def test_worker(self, mock_worker):
        mock_worker.return_value = "Hello, I'm worker"
        self.assertEqual(Main.worker(), "Hello, I'm worker", "Worker doesn't respond")

    def test_server_get(self):
        self.assertNotEqual(Main.server_get(), [], "Server doesn't send data")

    def test_worker_get(self):
        if Main.server_state == 1:
            self.assertEqual(Main.worker_get(),
                             {'state': 'PAUSE', 'task': [], 'main_dot': Main.main_dot, 'worker_number': -1})
        elif Main.server_state == 0:
            self.assertEqual(Main.worker_get(), {'state': 'STOP', 'task': [], 'main_dot': [], 'worker_number': -1})

        elif Main.server_state == 2:
            self.assertNotEqual(Main.worker_get(), {})

if __name__ == "__main__":
    unittest.main()