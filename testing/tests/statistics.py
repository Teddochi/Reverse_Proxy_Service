import requests
from ..context import proxy_url

def test(self):
	r = requests.get(proxy_url + "stats")
	test_stats_200(self, r)

	test_slow_requests(self)

def test_stats_200(self, response):
    self.assertEquals(r.status_code, 200)

def test_slow_requests(self):
	self.assertTrue(False)

def test_queries(self):
	self.assertTrue(False)