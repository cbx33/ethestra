import math
import random

DEFAULT_POSITION_MAPPINGS = [(0.99, 1.0, 1), (0.95, 0.99, 4), (0.7, 0.95, 8), (0, 0.7, 16)]
DEFAULT_PITCH_MAPPINGS = [(0, 0.2, None), (0.2, 1, "chord")]
DEBUG = 0

def __process_mod_stream(p, quant):
	di = p % quant
	if di > quant/2:
		di = -(quant - di)
	if DEBUG:
		print p, i, di, p+di, p - di
	return p - di

def ReturnNotePosition(mappings = DEFAULT_POSITION_MAPPINGS, bar_length = 4, bar_res = 16):

	p = random.random() * bar_res * bar_length
	j = random.random()
	for map in mappings:
		if j >= map[0] and j < map[1]:
			notepos = __process_mod_stream(p, map[2])
	return notepos
	
def ReturnNotePitch(mappings = DEFAULT_PITCH_MAPPINGS, notes = []):
	p = random.random()
	for map in mappings:
		if p >= map[0] and p < map[1]:
			if map[2] == None:
				return int(p * 12)
			else:
				return notes[int(len(notes) * p)]
	
def ReturnNoteVelocity(vel_dev):
	p = random.random()
	return (int(p * vel_dev) - (vel_dev / 2))
	
def ReturnNoteLength(percen, note_length, bar_res):
	if percen == 0:
		percen = 0.5
	print note_length / percen * bar_res
	return note_length / percen * bar_res
		
	
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
