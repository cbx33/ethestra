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

def PlayBar(self):
	"""
	This code implemented a single scheduler for notes, but this 
	does not work if the bars are different lengths, which could
	be the case

	temp_channel_data = []
	for channel in self.channels:
		temp_channel_data.append([channel.channel, channel.pattern])
	flag = 1
	while flag == 1:
		for channel_data in temp_channel_data:
			flag = 0
			if len(channel_data[1]) != 0:
				flag = 1
				note = channel_data[1].pop(0)
				current_channel = self.GetChannel(channel_data[0])
				
				gobject.timeout_add(current_channel.TimeForBeat(note[0]), current_channel.PlayNote, note[1], note[2])

				print note
	gobject.timeout_add(current_channel.TimeForBeat(current_channel.bar_length), self.PlayBar)
	"""
