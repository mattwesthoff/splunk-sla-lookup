import unittest
from sla_lookup import xrow_matches, is_staging

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

if __name__ == '__main__':
    unittest.main()