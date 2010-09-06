import math
import random

bar_length = 4
bar_res = 64

def process_mod(p, quant):
	mod = 0.0
	mod2 = 0.0
	while int(p-mod) % quant != 0:
		print p, int(p-mod), p % quant
		mod = mod - 1
	while int(p-mod2) % quant != 0:
		print p, int(p-mod2), p % quant
		mod2 = mod2 + 1
	print mod, mod2, min(abs(mod), abs(mod2)), int(p-min(abs(mod), abs(mod2)))
	return int(p-min(abs(mod), abs(mod2)))

notes = {}

for i in range(1000):
	p = random.random() * bar_res
	j = random.random()
	if j > .99:
		notepos = process_mod(p, 1)
	elif j <= 0.99 and j > .95:
		notepos = process_mod(p, 4)
	elif j <= 0.95 and j > 0.8:
		notepos = process_mod(p, 8)
	else:
		notepos = process_mod(p, 16)
	if notes.has_key(notepos):
		notes[notepos] += 1
	else:
		notes[notepos] = 1
		
for key in sorted(notes.iterkeys()):
	print key, notes[key]
	
