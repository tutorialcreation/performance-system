from django.test import TestCase
import unittest
# Create your tests here.

class TestSum(TestCase):
    def test_sum(self, *args):
        self.assertEqual(sum([1,2,3]),6, "should be 6")


if __name__ == "__main__":
    # TestSum()
    unittest.main()