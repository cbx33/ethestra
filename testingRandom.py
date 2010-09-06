import math
import random

bar_length = 4
bar_res = 64



for i in range(100):
	mod = 0.0
	mod2 = 0.0
	p = random.random() * bar_res
	j = random.random()
	if j > .95:
		while int(p-mod) % 4 != 0:
			print p, int(p-mod), p % 4
			mod = mod - 1
		while int(p-mod2) % 4 != 0:
			print p, int(p-mod2), p % 4
			mod2 = mod2 + 1
		print mod, mod2, min(abs(mod), abs(mod2)), int(p-min(abs(mod), abs(mod2)))
		notepos = bar_res
	elif j <= 0.95 and j > 0.8:
		notepos = bar_res
	else:
		notepos = bar_res
	
