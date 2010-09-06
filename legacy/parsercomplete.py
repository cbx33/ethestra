from pyparsing import *

integer = Word(nums).setParseAction(lambda t:int(t[0]))
ipaddress = Combine(Word(nums) + ('.' + Word(nums))*3)
parameter = oneOf('ip sport dport proto type').setParseAction(lambda t:"*"+t[0])
proto = oneOf('TCP UDP IP')
pkttype = oneOf('ICMP LLC ARP').setParseAction(lambda t:"#"+t[0])
operand = ipaddress | integer | parameter | proto | pkttype

operator = oneOf('AND OR')
comparitor = oneOf('== > < !=')
exister = Literal('IS')

expression = operatorPrecedence( operand,
    [("IS", 1, opAssoc.RIGHT),
     (comparitor, 2, opAssoc.RIGHT),
     (operator, 2, opAssoc.RIGHT),]
    )

class Packet():
	def __init__(self):
		self.ip = "10.0.0.0"
		self.dport = 0
		self.sport = 4
		self.proto = "TCP"
	def __getitem__(self, name):
		return vars(self)[name]
		
def Operation(value1, operator, value2, data):
	print "I've been called with", operator,":", value1,":", value2
	print "Types", type(value1), type(value2)
	
	if type(value1).__name__ == "str":
		if "*" in value1:
			value1 = data[value1[1:]]
	if type(value2).__name__ == "str":
		if "*" in value2:
			value2 = data[value2[1:]]
	print "Final:", value1, operator, value2
		
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
	print "Checking: " ,logic
	print "\tOperator: ",logic[1]
	print "\tArg1:", logic[0]
	print "\tArg2:", logic[2]
	if type(logic[0]).__name__ == "ParseResults":
		print "Arg1 is expression"
		logic[0] = Check(logic[0], data)
	if type(logic[2]).__name__ == "ParseResults":
		print "Arg2 is expression"
		logic[2] = Check(logic[2], data)
	return Operation(logic[0], logic[1], logic[2], data)
		
packet = Packet()

stri = "((*ip == 10.0.0.0) AND ((*sport < 3) OR (*proto == TCP))) AND (*proto == TCP)"
#stri = "(*ip == 10.0.0.0 AND *sport < 3) OR *proto == TCP"
stri = "sport == sport"
stri = "IS LLC"

arrays = expression.parseString(stri)
print len(arrays[0])
print len(arrays[0][0])
print "Sending:", arrays[0]
#print arrays
print Check(arrays[0], packet)
