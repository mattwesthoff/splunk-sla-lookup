import unittest
from sla_lookup import xrow_matches, is_staging, lookup
from datetime import datetime

class xRowMatchesTests(unittest.TestCase):
	def test_allwild(self):
		self.assertTrue(xrow_matches("javelin.staging.zsservices.com/client/0001a", ["*", "*", "*"]))

	def test_correctenv(self):
		self.assertTrue(xrow_matches("javelin.staging.zsservices.com/client/0001a", ["Stg", "*", "*"]))
	
	def test_correctgroup(self):
		self.assertTrue(xrow_matches("javelin.staging.zsservices.com/client/0001a", ["*", "*", "client"]))

	def test_correctapp(self):
		self.assertTrue(xrow_matches("javelin.staging.zsservices.com/client/0001a", ["*", "0001", "*"]))

	def test_allspecified(self):
		self.assertTrue(xrow_matches("javelin.staging.zsservices.com/client/0001a", ["Stg", "0001a", "client"]))

class isStagingTests(unittest.TestCase):
	def test_staging(self):
		self.assertTrue(is_staging("staging"))

	def test_prod(self):
		self.assertFalse(is_staging("javelin.zsservices"))

	def test_blank(self):
		self.assertFalse(is_staging(""))

class lookupTests(unittest.TestCase):

	def setUp(self):
		self.event_time = 1350421479 #Tue Oct 16 2012 16:04:39 GMT-5
		self.test_name = "javelin.zsservices.com/Amgen/0002a/tacos"

	def test_windowmatches(self):
		windows = [[("*","*","*"), datetime(2012,10,16,14,0,0), datetime(2012,10,16,17,0,0)]]
		self.assertTrue(lookup(self.test_name, self.event_time, windows))

	def test_shouldnotmatchtestname(self):
		windows = [[("Stg","0012","*"), datetime(2012,10,16,14,0,0), datetime(2012,10,16,17,0,0)]]
		test_name = "javelin.zsservices.com/Amgen/0002a/tacos"
		self.assertFalse(lookup(self.test_name, self.event_time, windows))

	def test_shouldnotmatchdates(self):
		windows = [[("*","*","*"), datetime(2012,10,14,14,0,0), datetime(2012,10,14,17,0,0)]]
		test_name = "javelin.zsservices.com/Amgen/0002a/tacos"
		self.assertFalse(lookup(self.test_name, self.event_time, windows))

	def test_matchesmanywindows(self):
		windows = [
			[("*","*","*"), datetime(2012,10,16,14,0,0), datetime(2012,10,16,17,0,0)],
			[("Prod","*","Amgen"), datetime(2012,10,16,14,0,0), datetime(2012,10,16,17,0,0)]
		]
		test_name = "javelin.zsservices.com/Amgen/0002a/tacos"
		self.assertTrue(lookup(self.test_name, self.event_time, windows))

if __name__ == '__main__':
    unittest.main()