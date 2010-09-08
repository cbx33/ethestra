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
