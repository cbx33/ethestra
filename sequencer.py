import portmidizero
import time
import gobject

DRUM_PATTERN = ([
	(0, 0x24, 0x60, 4), 
	(2, 0x24, 0x60, 4), 
	(8, 0x24, 0x60, 4), 

	(16, 0x27, 0x60, 4), 

	(0, 0x2A, 0x60, 4),
	(8, 0x2A, 0x60, 4),
	(16, 0x2A, 0x60, 4),
	(24, 0x2A, 0x60, 4),
	(32, 0x2A, 0x60, 4),
	(40, 0x2A, 0x60, 4),
	(48, 0x2A, 0x60, 4),
	(56, 0x2A, 0x60, 4),
	])
	
BASIC_PATTERN = [
	(48, 0x50, 0x60, 4), 
	(32, 0x53, 0x60, 4), 
	(16, 0x50, 0x60, 4), 
	(0, 0x57, 0x60, 4)]

class Seq(gobject.GObject):
	
	__gsignals__ = {
        'bar-fin': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
		}
	
	def __init__(self, device_name = "ZynAddSubFX"):
		self.tempo = 120
		self.channels = []
		self.control_channel = 1
		self.control_channel_cur = 0
		self.device = self.MidiDevice(device_name)
		self.global_pattern = []
		gobject.GObject.__init__(self)
		gobject.type_register(self.Channel)
		print "Starting Sequencer..."

	def AddChannel(self, chan, name="Blank", modable=1):
		self.channels.append(self.Channel(self.device, chan, self.tempo, name, modable))
		self.GetChannel(chan).connect("bar-end", self.BarEndHandler, chan)
	
	def BarEndHandler(self, o, chan):
		if chan == self.control_channel:
			if self.control_channel_cur > len(self.global_pattern)+1:
				self.control_channel_cur = 0
			if len(self.global_pattern) > 0:
				for channel in self.channels:
					if channel.modable != 0:
						channel.tran_mod = self.global_pattern[1][self.control_channel_cur]
			self.control_channel_cur += 1
			print "Bar End============================"
			self.emit("bar-fin")
		
	def DeleteChannel(self, chan):
		"Not Yet Implemented"

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
		
		for channel in self.channels:
			channel.PlayBar()
		
	def Summary(self):
		print "Chan\tName\tLength"
		print "==========================================="
		for channel in self.channels:
			print str(channel.channel) + "\t" + str(channel.name) + "\t" + str(channel.bar_length)
		
	def GetChannel(self, number):
		for channel in self.channels:
			if channel.channel == number:
				return channel
				
	def SetGlobalControlPattern(self, pattern):
		self.global_pattern = pattern
		
	def SetTempo(self, tempo):
		self.tempo = tempo
		
	def GetTempo(self):
		return self.tempo

	class MidiDevice():
		def __init__(self, device_name = "ZynAddSubFX"):
			self.device_name = device_name
			self.device = None
			self.OpenDevice()

		def OpenDevice(self):
			for loop in range(portmidizero.CountDevices()):
				interf,name,inp,outp,opened = portmidizero.GetDeviceInfo(loop)
				if outp == 1 and name == self.device_name:
				   self.device = portmidizero.Output(loop,0)

		def TestDevice(self):
			self.device.WriteShort(0x90,0x50+3,0x60)
			time.sleep(0.1)
			self.device.WriteShort(0x80,0x50+3,0x60)
			
		def Write(self, mess, note, velo):
			try:
				self.device.WriteShort(mess, note, velo)
			except AttributeError:
				pass
	
	class Channel(gobject.GObject):
		
		__gsignals__ = {
		'bar-end': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
			}
        
		def __init__(self, device, channel, tempo, name="Blank", modable=1):
			self.name = name
			self.modable = modable
			self.pattern = [(0, 0x50, 0x60, 4), (16, 0x53, 0x60, 4), (32, 0x50, 0x60, 4), (48, 0x57, 0x60, 4)]
			self.tempo = tempo
			self.channel = channel
			self.device = device
			self.note_length = 1
			self.bar_length = 4
			self.bar_res = 16
			self.cur_point = 0
			self.pattern = sorted(self.pattern, key=lambda pat: pat[0])
			self.mute = 0
			self.transpose = 0
			self.tran_mod = 0
			gobject.GObject.__init__(self)

			
		def TestPlay(self):
			self.device.Write(0x90+self.channel-1,0x50+self.transpose+self.tran_mod,0x60)
			time.sleep(0.1)
			self.device.Write(0x80+self.channel-1,0x50+self.transpose+self.tran_mod,0x60)
			
		def Mute(self):
			self.mute = 1
			
		def UnMute(self):
			self.mute = 0

		def PlayBar(self):
			if self.mute == 0:
				for note in self.pattern:
					#print self.TimeForBeat(note[0])
					gobject.timeout_add(int(self.TimeForBeat(note[0])), self.PlayNote, note[1] + self.transpose + self.tran_mod, note[2], note[3])
			gobject.timeout_add(int(self.TimeForBeat(self.bar_res)) * self.bar_length, self.PlayBar)
			self.emit('bar-end')
				
		def PlayNote(self, note, velo, length):
			self.NoteOn(note, velo)
			gobject.timeout_add(int(self.TimeForBeat(self.note_length)) * length, self.NoteOff, note, velo)
			
		def TimeForBeat(self, numbeat):
			return float(60) / float(self.tempo) / self.bar_res * 1000.0 * float(numbeat)
			
		def NoteOn(self, note, velo):
			#print "Note on", note, velo
			self.device.Write(0x90+self.channel-1, note, velo)
			
		def NoteOff(self, note, velo):
			#print "Note off", note, velo
			self.device.Write(0x80+self.channel-1, note, velo)
		
		def AddPattern(self, pattern):
			sorted_pattern = sorted(pattern, key=lambda pat: pat[0])
			self.pattern = sorted_pattern
	
def Demo():
	seq = Seq()
	seq.SetTempo(100)
	print seq.tempo
	seq.SetGlobalControlPattern([1, (0, 5, 4, 7)])
	seq.AddChannel(1, name="Totoro")
	seq.AddChannel(2)
	seq.AddChannel(3)
	seq.AddChannel(10, name="Drums", modable=0)
	seq.GetChannel(3).transpose = -36

	seq.GetChannel(2).AddPattern([(48, 0x50, 0x60, 4), (32, 0x53, 0x60, 4), (16, 0x50, 0x60, 4), (0, 0x57, 0x60, 4)])
	seq.GetChannel(3).AddPattern([(0, 0x50, 0x60, 64)])
	seq.GetChannel(10).AddPattern([
	(0, 0x24, 0x60, 4), 
	(2, 0x24, 0x60, 4), 
	(8, 0x24, 0x60, 4), 

	(16, 0x27, 0x60, 4), 

	(0, 0x2A, 0x60, 4),
	(8, 0x2A, 0x60, 4),
	(16, 0x2A, 0x60, 4),
	(24, 0x2A, 0x60, 4),
	(32, 0x2A, 0x60, 4),
	(40, 0x2A, 0x60, 4),
	(48, 0x2A, 0x60, 4),
	(56, 0x2A, 0x60, 4),
	])
	seq.PlayBar()
	seq.Summary()

	Loop = gobject.MainLoop()
	Loop.run()

if __name__ == '__main__':
	Demo()

"""
a = gtk.Window()
b = gtk.Button("Close")
a.add(b)
b.connect("clicked", Loop.quit)
a.show_all()
"""

