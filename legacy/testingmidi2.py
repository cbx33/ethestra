import portmidizero
import time
import gobject
import gtk

class MidiDevice():
	def __init__(self):
		self.device = None
		self.OpenDevice()

	def OpenDevice(self):
		""" """
		for loop in range(portmidizero.CountDevices()):
			interf,name,inp,outp,opened = portmidizero.GetDeviceInfo(loop)
			if outp == 1 and name == "ZynAddSubFX":
			   self.device = portmidizero.Output(loop,0)

	def TestDevice(self):
		self.device.WriteShort(0x90,0x50+3,0x60)
		time.sleep(0.1)
		self.device.WriteShort(0x80,0x50+3,0x60)
		
	def Write(self, mess, note, velo):
		self.device.WriteShort(mess, note, velo)

class Seq():
	class Channel():
		def __init__(self, device, channel, name="Blank"):
			self.name = name
			self.pattern = [(0, 0x50, 0x60, 4), (16, 0x53, 0x60, 4), (32, 0x50, 0x60, 4), (48, 0x57, 0x60, 4)]
			self.tempo = 100
			self.channel = channel
			self.device = device
			self.note_length = 1
			self.bar_length = 4
			self.bar_res = 16
			self.cur_point = 0
			self.pattern = sorted(self.pattern, key=lambda pat: pat[0])
			self.mute = 0
			self.transpose = 0
			
		def TestPlay(self):
			self.device.Write(0x90+self.channel-1,0x50+self.transpose,0x60)
			time.sleep(0.1)
			self.device.Write(0x80+self.channel-1,0x50+self.transpose,0x60)
			
		def Mute(self):
			self.mute = 1
			
		def UnMute(self):
			self.mute = 0

		def PlayBar(self):
			if self.mute == 0:
				for note in self.pattern:
					#print self.TimeForBeat(note[0])
					gobject.timeout_add(self.TimeForBeat(note[0]), self.PlayNote, note[1] + self.transpose, note[2], note[3])
			gobject.timeout_add(int(self.TimeForBeat(self.bar_res)) * self.bar_length, self.PlayBar)
				
		def PlayNote(self, note, velo, length):
			self.NoteOn(note, velo)
			gobject.timeout_add(int(self.TimeForBeat(self.note_length)) * length, self.NoteOff, note, velo)
			
		def TimeForBeat(self, numbeat):
			return float(60) / float(self.tempo) / self.bar_res * 1000.0 * float(numbeat)
			
		def NoteOn(self, note, velo):
			print "Note on", note, velo
			self.device.Write(0x90+self.channel-1, note, velo)
			
		def NoteOff(self, note, velo):
			print "Note off", note, velo
			self.device.Write(0x80+self.channel-1, note, velo)
		
		def AddPattern(self, pattern):
			sorted_pattern = sorted(pattern, key=lambda pat: pat[0])
			self.pattern = sorted_pattern
	
	def __init__(self):
		self.channels = []
		self.device = MidiDevice()
		self.global_pattern = []
		print "Starting Sequencer..."

	def AddChannel(self, chan, name="Blank"):
		self.channels.append(seq.Channel(self.device, chan, name))
	
	def DeleteChannel(self, chan):
		"Not Yet Implemented"

	def PlayBar(self):
		"""
		This code implemented a single scheduler for notes, but this 
		does not work if the bars are different lengths, which could
		be the case
		"""
		"""
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
		
	


seq = Seq()
seq.SetGlobalControlPattern([1, (0, 5, 3, 7)])
seq.AddChannel(1, name="Totoro")
seq.AddChannel(2)
seq.AddChannel(3)
seq.AddChannel(10, name="Drums")
#seq.GetChannel(1).Mute()
#seq.GetChannel(2).Mute()
#seq.GetChannel(3).Mute()
seq.GetChannel(3).transpose = -36

seq.GetChannel(2).AddPattern([(48, 0x50, 0x60, 4), (32, 0x53, 0x60, 4), (16, 0x50, 0x60, 4), (0, 0x57, 0x60, 4)])
seq.GetChannel(3).AddPattern([(0, 0x50, 0x60, 64)])
seq.GetChannel(10).transpose = -36
seq.GetChannel(10).AddPattern([
(0, 0x48, 0x60, 4), 
(2, 0x48, 0x60, 4), 
(8, 0x48, 0x60, 4), 

(16, 0x4B, 0x60, 4), 

(0, 0x4E, 0x60, 4),
(8, 0x4E, 0x60, 4),
(16, 0x4E, 0x60, 4),
(24, 0x4E, 0x60, 4),
(32, 0x4E, 0x60, 4),
(40, 0x4E, 0x60, 4),
(48, 0x4E, 0x60, 4),
(56, 0x4E, 0x60, 4),
])
seq.PlayBar()
seq.Summary()


Loop = gobject.MainLoop()
Loop.run()

"""
a = gtk.Window()
b = gtk.Button("Close")
a.add(b)
b.connect("clicked", Loop.quit)
a.show_all()
"""

