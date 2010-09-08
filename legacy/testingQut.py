for i in range(64):
	di = i % 16
	if di > 16/2:
		di = -(16 - di)
	print i, di, i+di, i - di

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
