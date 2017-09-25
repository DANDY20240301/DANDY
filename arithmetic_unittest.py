import unittest
import arithmetic
from fractions import Fraction

class ArithmeticTest(unittest.TestCase):
	#setup
	def setup(self):
		pass

	def testExpression(self):
		# 随机10000次，用eval()函数判断表达式是否合法
		for x in range(1,10000):
			expr = arithmetic.expression()
			result = type(eval(("".join(expr[:-1])).replace('÷','/')))
			flag = 0
			if result == float:
				flag = 1
			elif result == int:
				flag = 1
			self.assertEqual(flag,1)
		print("test expression() pass")

	def testToSuffix(self):
		# 生成9条测试语句，基本覆盖+、-、*、÷、整数、分数、括号的情况
		self.assertEqual(arithmetic.tosuffix(['3', '+', '12', '/', '12', '+', '12', '+', '17', '=']),[3, Fraction(1, 1), '+', 12, '+', 17, '+'])
		self.assertEqual(arithmetic.tosuffix(['4', '*', '17', '/', '14', '*', '4', '+', '7', '-', '12', '/', '20', '-', '4', '+', '14', '=']),[4, Fraction(17, 14), '*', 4, '*', 7, '+', Fraction(3, 5), '-', 4, '-', 14, '+'])
		self.assertEqual(arithmetic.tosuffix(['11', '/', '6', '÷', '5', '+', '0', '*', '4', '/', '6', '=']),[Fraction(11, 6), 5, '÷', 0, Fraction(2, 3), '*', '+'])
		self.assertEqual(arithmetic.tosuffix(['18', '/', '15', '÷', '9', '/', '10', '*', '5', '-', '18', '*', '3', '÷', '18', '=']),[Fraction(6, 5), Fraction(9, 10), '÷', 5, '*', 18, 3, '*', 18, '÷', '-'])
		self.assertEqual(arithmetic.tosuffix(['5', '+', '7', '÷', '(', '14', '-', '20', '÷', '9', '÷', '13', '÷', '7', '-', '3', '+', '12', ')', '*', '13', '=']),[5, 7, 14, 20, 9, '÷', 13, '÷', 7, '÷', '-', 3, '-', 12, '+', '÷', 13, '*', '+'])
		self.assertEqual(arithmetic.tosuffix(['10', '/', '19', '÷', '9', '-', '0', '=']),[Fraction(10, 19), 9, '÷', 0, '-'])
		self.assertEqual(arithmetic.tosuffix(['18', '+', '(', '13', '+', '18', '*', '4', '*', '17', ')', '*', '3', '+', '19', '/', '20', '-', '14', '*', '5', '=']),[18, 13, 18, 4, '*', 17, '*', '+', 3, '*', '+', Fraction(19, 20), '+', 14, 5, '*', '-'])
		self.assertEqual(arithmetic.tosuffix(['0', '/', '6', '-', '12', '*', '(', '8', '/', '2', ')', '+', '16', '=']),[Fraction(0, 1), 12, Fraction(4, 1), '*', '-', 16, '+'])
		self.assertEqual(arithmetic.tosuffix(['12', '*', '(', '9', '*', '20', ')', '-', '16', '=']),[12, 9, 20, '*', '*', 16, '-'])
		print("test tosuffix() pass")

	def testCalculate(self):
		# 生成7条测试语句，包含的结果类型覆盖正负整数和分数
		self.assertEqual(arithmetic.calculate([5, Fraction(7, 9), 18, '*', '-', 18, 20, '÷', '-']),Fraction(-99,10))
		self.assertEqual(arithmetic.calculate([1, 15, 19, '÷', 8, '÷', 13, '÷', 14, '*', '-', 15, 2, '*', '-']),Fraction(-28757,988))
		self.assertEqual(arithmetic.calculate([18, 16, '+']),34)
		self.assertEqual(arithmetic.calculate([6, Fraction(16, 11), 11, '÷', '-', 5, 10, 5, '÷', '-', 3, '÷', '+']),Fraction(831,121))
		self.assertEqual(arithmetic.calculate([12, 5, '-', Fraction(5, 18), '-', Fraction(13, 5), '+']),Fraction(839,90))
		self.assertEqual(arithmetic.calculate([17, 16, '*', 17, '+', 11, 16, '*', '-', 13, 11, '*', 0, '*', '+', 4, '-']),109)
		self.assertEqual(arithmetic.calculate([4, Fraction(1, 1), '*', 8, '-']),-4)
		print("test calculate() pass")

def main():
	suite = unittest.TestSuite()
	suite.addTest(ArithmeticTest("testExpression"))
	suite.addTest(ArithmeticTest("testToSuffix"))
	suite.addTest(ArithmeticTest("testCalculate"))

	runner = unittest.TextTestRunner()
	runner.run(suite)

if __name__ == '__main__':
	main()