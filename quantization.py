import math
import random

DEFAULT_MAPPINGS = [(0.99, 1), (0.95, 4), (0.8, 8), (0, 16)]

def __process_mod(p, quant):
	mod = 0.0
	mod2 = 0.0
	while int(p-mod) % quant != 0:
		#print p, int(p-mod), p % quant
		mod = mod - 1
	while int(p-mod2) % quant != 0:
		#print p, int(p-mod2), p % quant
		mod2 = mod2 + 1
	#print mod, mod2, min(abs(mod), abs(mod2)), int(p-min(abs(mod), abs(mod2)))
	return int(p-min(abs(mod), abs(mod2)))

def ReturnNote(mappings = DEFAULT_MAPPINGS, bar_length = 4, bar_res = 16):

	p = random.random() * bar_res * bar_length
	j = random.random()
	if j > mappings[0][0]:
		notepos = __process_mod(p, mappings[0][1])
	elif j <= mappings[0][0] and j > mappings[1][0]:
		notepos = __process_mod(p, mappings[1][1])
	elif j <= mappings[1][0] and j > mappings[2][0]:
		notepos = __process_mod(p, mappings[2][1])
	else:
		notepos = __process_mod(p, mappings[3][1])
	return notepos
	
if __name__ == '__main__':
	notes = {}

	for i in range(1000):
		notepos = ReturnNote()
		if notes.has_key(notepos):
			notes[notepos] += 1
		else:
			notes[notepos] = 1
			
	for key in sorted(notes.iterkeys()):
		print key, notes[key]
