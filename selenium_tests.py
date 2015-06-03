__author__ = 'oleh'

from selenium import webdriver
import unittest


class DotsCounterTest(unittest.TestCase):

    def test_server(self):
        print "TESTING SERVER"
        driver = webdriver.Firefox()
        driver.get("http://localhost:8080/server")

        self.assertEqual(driver.title, "__SERVER__", "Can't access Server.html")

        page = driver.find_element_by_tag_name("body").text
        assert "Clients" in page
        assert "Percentage" in page
        assert "Time taken" in page
        assert "Closest dot" in page

    def test_worker(self):
        print "TESTING WORKER"
        driver = webdriver.Firefox()
        driver.get("http://localhost:8080/worker")

        self.assertEqual(driver.title, "__CLIENT__", "Can't access Worker.html")

        page = driver.find_element_by_tag_name("body").text
        assert "Dots to calculate" in page
        assert "Last min way" in page


if __name__ == "__main__":
    unittest.main()