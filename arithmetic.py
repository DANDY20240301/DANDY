import sys,getopt
import random
from matplotlib.cbook import flatten
from itertools import chain
from fractions import Fraction
import os,copy
import math

# 定义运算符优先级
priority = {'+':1,'-':1,'*':2,'÷':2}

# 生成表达式
def expression():
	opts = ['+','-','*','÷','/']
	op = [] # 运算符列表
	tmp = [] # 表达式列表
	num_op = random.randint(1,9) # 附加功能：生成不定长运算符个数
	# 生成算式
	preoperand = 0
	preop = ''
	for i in range(num_op+1):
		if preop == '÷':
			preoperand = random.randint(1,5) # 防止除数为0
			preop = opts[random.randint(0, 4)]
		elif preop == '/':
			preoperand = random.randint(1,5)
			preop = opts[random.randint(0, 3)] # 防止连续两个/,如3/4/5
		else:
			preoperand = random.randint(0,5)
			preop = opts[random.randint(0, 4)] 
		tmp.append(str(preoperand))
		tmp.append(preop)
	no_bracket = tmp.copy()

	# 加括号
	try:
		left1_pos = random.randint(0,len(tmp)-4) # 限定左括号位置
		right1_pos = random.randint(left1_pos+3,len(tmp)-2) # 限定右括号位置
		tmp.insert(left1_pos,'(')
		tmp.insert(right1_pos,')')
		print("".join(tmp[:-1]))
	except Exception:
		no_bracket[-1] = "="
		return no_bracket

	flag1 = 0 # 标记是否有"/"
	index_list = [] # 有/的下标列表
	for i in range(len(tmp)-1):
		if tmp[i] == '/':
			flag1 =flag1 + 1
			# index_list.append(tmp.index(i)) # 只索引第一个/
			index_list.append(i)
	
	# 如果没有/
	if flag1 == 0:
		try:
			eval(("".join(tmp[:-1])).replace('÷','/'))
			# print("".join(tmp[:-1]))
			tmp[-1] = "="
			# print("无/加（）")
			return tmp
		except Exception:
			no_bracket[-1] = "="
			return no_bracket
	# 如果有/
	else:
		for i in index_list:
			print(tmp[i-1:i+2],index_list)
			if tmp[i-1].isdigit() and tmp[i+1].isdigit(): # 用了两次index
				try:
					eval(("".join(tmp[:-1])).replace('÷','/')) #判断带括号的式子是否合法
					# print("有/加（）")
				except Exception:
					# print("有/不加（）")
					no_bracket[-1] = "="
					return no_bracket
			else:
				no_bracket[-1] = "="
				return no_bracket
		tmp[-1] = "="	
		return tmp  # 防止第一个正确 第二个蒙混过关
	
# 把中缀表达式转为后缀表达式
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
		print(suffix)
		print(stack)
		if type(e) != str: 
			suffix.append(e)
		elif e.isdigit(): # 操作数
			suffix.append(int(e))
		elif e == ')': # 右括号
			tmp_pop = ''
			while tmp_pop != '(':
				tmp_pop = stack.pop()
				if tmp_pop != '(':
					suffix.append(tmp_pop)
		elif len(stack) == 0 or stack[-1] == '(' or e == '(': # 左括号
			stack.append(e)
		else: #其他运算符
			while(len(stack) and stack[-1] != '(' and priority[stack[-1]] >= priority[e]): # stack[-1] == '(' stack[-1] != '(' 可变优先级
				suffix.append(stack.pop())
			stack.append(e)
	while len(stack): # 把栈弹干净
		suffix.append(stack.pop())
	return suffix

# 后缀表达式求值
def calculate(suffix):
	print(suffix)
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
	print(calStack[0])
	return calStack.pop()

# 基本运算
def doMath(op,op1,op2):
	if op == '+':
		return op1+op2
	elif op == '-':
		return op1-op2
	elif op == '*':
		return op1*op2
	elif op == '÷':
		return Fraction(op1,op2)

# 主函数
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

	# 计算成绩
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
			print("回答正确！\n")
		else:
			print("回答错误！,正确答案是{}\n".format(calculate(suffix)))
	print("共答对{}题".format(flag)+"," "本次得分：{}".format(round(each_score*flag)))
		
	
if __name__ == '__main__':
	main(sys.argv[1:])