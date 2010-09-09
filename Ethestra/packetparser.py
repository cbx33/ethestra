from pyparsing import *
from scapy.all import *

DEBUG = 0

integer = Word(nums).setParseAction(lambda t:int(t[0]))
ipaddress = Combine(Word(nums) + ('.' + Word(nums))*3)
parameter = oneOf('src dst sport dport proto type chump').setParseAction(lambda t:"*"+t[0])
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

def Operation(data, value1, operator, value2 = None):
	if DEBUG:
		print "I've been called with", operator,":", value1,":", value2
		print "Types", type(value1), type(value2)
	if type(value1).__name__ == "str":
		if "*" in value1:
			try:
				value1 = getattr(data, value1[1:])
			except (KeyError, AttributeError):
				return False
		elif "#" in value1:
			value1 = value1[1:]
			value1 = getattr(scapy.all, value1)
	if type(value2).__name__ == "str":
		if "*" in value2:
			try:
				value2 = getattr(data, value2[1:])
			except (KeyError, AttributeError):
				return False
	if DEBUG:
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
	elif operator == "IS":
		return value1 in data
		
def FilterCheck(logic, data):
	if DEBUG:
		print "Checking: " ,logic
		print "\tOperator: ",logic[1]
		print "\tArg1:", logic[0]
		print len(logic)
	if len(logic) == 2:
		if DEBUG:
			print "Invoking 2bit operation"
		return Operation(data, operator = logic[0], value1 = logic[1])
	else:
		if DEBUG:
			print "\tArg2:", logic[2]
		if type(logic[0]).__name__ == "ParseResults":
			if DEBUG:
				print "Arg1 is expression"
			logic[0] = FilterCheck(logic[0], data)
		if type(logic[2]).__name__ == "ParseResults":
			if DEBUG:
				print "Arg2 is expression"
			logic[2] = FilterCheck(logic[2], data)
		if DEBUG:
			print "Invoking 3bit operation"
			print logic[2]
		return Operation(data, operator = logic[1], value1 = logic[0], value2 = logic[2])
		
def ParseFilter(filter_string):
	return expression.parseString(filter_string)
		
if __name__ == "__main__":
	class Packet():
		def __init__(self):
			self.dst = "10.0.0.0"
			self.src = "10.0.0.0"
			self.dport = 0
			self.sport = 4
			self.proto = "TCP"
		def __getitem__(self, name):
			return vars(self)[name]
	packet = Packet()

	stri = "((*ip == 10.0.0.0) AND ((*sport < 3) OR (*proto == TCP))) AND (*proto == TCP)"

	arrays = ParseFilter(stri)
	print arrays
	print len(arrays[0])
	print len(arrays[0][0])
	print "Sending:", arrays[0]
	print FilterCheck(arrays[0], packet)
