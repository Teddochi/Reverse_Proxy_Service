import os

def test(self):
	run_script_exists(self)
	tests_script_exists(self)
	readme_exists(self)

def run_script_exists(self):
	self.assertTrue(os.path.isfile("Run.sh"))

def tests_script_exists(self):
	self.assertTrue(os.path.isfile("Tests.sh"))

def readme_exists(self):
	self.assertTrue(os.path.isfile("README.md"))