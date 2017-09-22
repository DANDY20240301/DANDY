import sys,getopt
import random
from matplotlib.cbook import flatten
from itertools import chain
from fractions import Fraction
import os

# 定义运算符优先级
priority = {'+':1,'-':1,'*':2,'÷':2,'(':3,')':0}

def expression():
	opts = ['+','-','*','÷','/']

	# 每个式子
	op = [] # 运算符列表
	# operand = [] #操作数列表
	tmp = []
	# fomula = ""
	num_op = random.randint(1,9) # 附加功能：生成不定长运算符个数
	# 生成算式
	preoperand = 0
	preop = ''
	for i in range(num_op+1):
		if preop == "÷":
			preoperand = random.randint(1,5) # 防止除数为0
			preop = opts[random.randint(0, 4)]
		elif preop == "/":
			preoperand = random.randint(1,5)
			preop = opts[random.randint(0, 3)] # 防止连续两个/,如3/4/5
		else:
			preoperand = random.randint(0,5)
			preop = opts[random.randint(0, 4)] 
		tmp.append(str(preoperand))
		tmp.append(preop)
	tmp[-1] = "="
		
	return tmp

def tosuffix(expr):
	new_list = []
	# 把分数单独作为一种操作数
	i = 0
	while (i<(len(expr)-1)):
		if expr[i+1] == '/':
			new_list.append(Fraction(int(expr[i]),int(expr[i+2])))
			i = i+3
		else :
			new_list.append(expr[i])
			i = i+1
	suffix = [] # 后缀表达式
	stack = [] # 操作符栈
	for e in new_list:
		if type(e) != str: 
			suffix.append(e)
		elif e.isdigit(): # 操作数
			suffix.append(int(e))
		elif e == '(': # 左括号
			stack.append(e)
		elif e == ')': # 右括号
			while stack[-1] != '(':
				suffix.append(stack.pop())
			stack.pop()
		else: #其他运算符
			while(len(stack) and priority[stack[-1]] >= priority[e]):
				suffix.append(stack.pop())
			stack.append(e)
	while len(stack): # 把栈弹干净
		suffix.append(stack.pop())
	return suffix

def calculate(suffix):
	calStack = []
	for s in suffix:
		if type(s) == int:
			calStack.append(int(s))
		elif type(s) != str:
			calStack.append(s)
		else:
			operand2 = calStack.pop()
			operand1 = calStack.pop()
			result = doMath(s,operand1,operand2)
			calStack.append(result)
	return calStack.pop()

def doMath(op,op1,op2):
	if op == '+':
		return op1+op2
	elif op == '-':
		return op1-op2
	elif op == '*':
		return op1*op2
	elif op == '÷':
		return Fraction(op1,op2)

def main(argv):
	n = ''
	try:
		opts, args = getopt.getopt(argv,"hn:",["n="])
	except getopt.GetoptError:
		print ('输入格式：filename.py -n 5')
		print ('5 位为题目个数')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('usage: arithmetic.py -n num of question')
			sys.exit()
		elif opt in ("-n", "--n"):
			n = arg

	each_score = float(100/int(n))
	total_score = 0
	flag = 0

	print ("本次共 {} 题,满分 100 分".format(n))
	for x in range(1,int(n)+1):
		expr = expression()
		fomula = "".join(expr) # 把列表接在一起
		suffix = tosuffix(expr)
		print(str(x)+". "+fomula,end = '')
		ans = input()
		if ans == str(calculate(suffix)):
			flag+=1
			print("回答正确！")
		else:
			print("回答错误！")
	print("共答对{}题".format(flag)+"," "本次得分：{}".format(round(each_score*flag)))
		
	
if __name__ == '__main__':
	main(sys.argv[1:])