import requests
from app import constants

def test(self):
	r = requests.get(constants.proxy_url + constants.stats_path)
	test_stats_200(self, r)
	test_slow_requests(self)
	test_queries(self)

def test_stats_200(self, response):
    self.assertEquals(response.status_code, 200)

def test_slow_requests(self):
	self.assertTrue(False)

def test_queries(self):
	self.assertTrue(False)