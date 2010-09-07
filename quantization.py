import math
import random

DEFAULT_MAPPINGS = [(0.99, 1.0, 1), (0.95, 0.99, 4), (0.7, 0.95, 8), (0, 0.7, 16)]
DEBUG = 0

def __process_mod_stream(p, quant):
	di = p % quant
	if di > quant/2:
		di = -(quant - di)
	if DEBUG:
		print p, i, di, p+di, p - di
	return p - di

"""
def __process_mod(p, quant):	
	mod = 0.0
	mod2 = 0.0
	while int(p-mod) % quant != 0:
		if DEBUG:
			print p, int(p-mod), p % quant
		mod = mod - 1
	while int(p-mod2) % quant != 0:
		if DEBUG:
			print p, int(p-mod2), p % quant
		mod2 = mod2 + 1
	if DEBUG:
		print mod, mod2, min(abs(mod), abs(mod2)), int(p-min(abs(mod), abs(mod2)))
	return int(p-min(abs(mod), abs(mod2)))
"""

def ReturnNotePosition(mappings = DEFAULT_MAPPINGS, bar_length = 4, bar_res = 16):

	p = random.random() * bar_res * bar_length
	j = random.random()
	for map in mappings:
		if j >= map[0] and j < map[1]:
			notepos = __process_mod_stream(p, map[2])
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
