for i in range(64):
	di = i % 16
	if di > 16/2:
		di = -(16 - di)
	print i, di, i+di, i - di
