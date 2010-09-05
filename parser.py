from pyparsing import *

integer = Word(nums).setParseAction(lambda t:int(t[0]))
ipaddress = Combine(Word(nums) + ('.' + Word(nums))*3)
parameter = oneOf('ip sport dport proto')
proto = oneOf('TCP UDP IP')
operand = ipaddress | integer | parameter | proto

operator = oneOf('AND OR')
comparitor = oneOf('== > < !=')

expression = operatorPrecedence( operand,
    [(comparitor, 2, opAssoc.RIGHT),
     (operator, 2, opAssoc.RIGHT),]
    )

class Packet():
	def __init__(self):
		self.ip = "10.0.0.0"
		self.dport = "0"
		self.sport = "4"
		self.proto = "TCP"
	def __getitem__(self, name):
		return vars(self)[name]
		
def Operation(operator, value1, value2, data):
	print operator, value1, value2

	if type(value1).__name__ != "bool":
		if "*" in value1:
			value1 = data[value1[1:]]
	if type(value2).__name__ != "bool":
		if "*" in value2:
			value2 = data[value2[1:]]
		
	if operator == "AND":
		return value1 and value2
	elif operator == "OR":
		return value1 or value2
	elif operator == "==":
		return value1 == value2
	elif operator == ">":
		return value1 > value2
	elif operator == "<":
		return value1 < value2
	elif operator == "!=":
		return value1 != value2
		
def Check(logic, data):
	print logic
	if type(logic[1]).__name__ == "list":
		logic[1] = Check(logic[1], data)
	if type(logic[2]).__name__ == "list":
		logic[2] = Check(logic[2], data)
	return Operation(logic[0], logic[1], logic[2], data)
		
packet = Packet()

print Check(["AND", ["AND", ["==", "*ip", "10.0.0.0"], ["OR", ["<", "*sport", "3"], ["==", "*proto", "TCP"]]], ["!=", "*proto", "TCP"]], packet)
["AND", ["AND", ["==", "*ip", "10.0.0.0"], ["OR", ["<", "*sport", "3"], ["==", "*proto", "TCP"]]], ["!=", "*proto", "TCP"]]
stri = "((ip == 10.0.0.0) AND ((sport < 3) OR (proto == TCP))) AND (proto == TCP)"

"""
test2 = ['(ip == 10 AND (sport < 3 OR proto == TCP)) AND proto == TCP',
		'(ip == 10.12.12.12 AND (sport < 3 OR proto == TCP)) AND proto == TCP']

for t in test2:
    print t
    print expr2.parseString(t)
    print 
"""
arrays = expression.parseString(stri)
