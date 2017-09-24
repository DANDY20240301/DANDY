import unittest
import arithmetic
from fractions import Fraction

class ArithmeticTest(unittest.TestCase):
	#setup
	def setup(self):
		self.arithmetic = arithmetic.expression()

	def testExpression(self):

	def testToSuffix(self):
		self.assertEqual(arithmetic.tosuffix([1,2,3]),3)

	def testCalculate(self):

def main():
	suite = unittest.TestSuite()
	suite.addTest(ArithmeticTest("testExpression"))
	#suite.addTest(ArithmeticTest("testToSuffix"))
	#suite.addTest(ArithmeticTest("testCalculate"))

	runner = unittest.TextTestRunner()
	runner.run(suite)

if __name__ == '__main__':
	main()