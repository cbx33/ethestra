from scapy.all import *
import sequencer
import packetparser
import gobject
from threading import Thread
import random
import signal
import quantization as qtz

DISABLE_SNIFFER = 0
DEFAULT_ROOT_NOTE = 78
	
class Ethestra():
	def __init__(self, device_name, tempo = 100):
		gobject.threads_init()
		gobject.io_add_watch(sys.stdin,
                     gobject.IO_IN | gobject.IO_ERR | gobject.IO_HUP,
                     self.InputHandler)
		self.stop_flag = 0
		self.seq = sequencer.Seq(device_name)
		self.seq.SetTempo(tempo)
		self.instruments = []
	
	def Start(self):
		self.seq.PlayBar()
		self.seq.connect("bar-fin", self.FinishedBar)
		if not DISABLE_SNIFFER:
			self.sniffer_thread = Thread(target=self.StartSniffer, args=())
			self.sniffer_thread.start()
		Loop = gobject.MainLoop()
		Loop.run()
		
	def StartSniffer(self):
		sniff(prn=self.PacketHandler, store=0, stopper=self.StopperCheck, stopperTimeout=1)

	def InputHandler(self, fd, io_condition):
		self.stop_flag = 1
		self.sniffer_thread.join()
		exit(0)
		
	def StopperCheck(self):
		if self.stop_flag:
			return True
		else:
			return False
			
	def FinishedBar(self, e):
		for instrument in self.instruments:
			instrument.history.append(instrument.packet_count)
			if len(instrument.history) > instrument.history_length:
				instrument.history.pop(0)
			instrument.packet_ave = sum(instrument.history) / len(instrument.history)
			instrument.ResetPacketCount()
			if instrument.modable:
				note_pitch = qtz.ReturnNotePitch(notes = instrument.keynotes) + DEFAULT_ROOT_NOTE + instrument.transpose
				note_position = qtz.ReturnNotePosition(bar_length = instrument.bar_length, bar_res = instrument.bar_res)
				note_velocity = qtz.ReturnNoteVelocity(instrument.velocity_deviation) + 96
				try:
					note_length = qtz.ReturnNoteLength(float(instrument.history[len(instrument.history) - 1]) / float(instrument.packet_ave), instrument.note_length, instrument.bar_length)
				except ZeroDivisionError:
					note_length = qtz.ReturnNoteLength(0, instrument.note_length, instrument.bar_length)
				print note_length , "**"
				if note_length == 0:
					note_length = 1
				instrument.channel.pattern.append((note_position, note_pitch, note_velocity, int(note_length)))			
			print instrument.history, instrument.packet_ave, instrument.pattern, note_pitch, note_position
		
	def PacketHandler(self, pkt):
		print pkt.summary()
		for instrument in self.instruments:
			if packetparser.FilterCheck(instrument.compiled_filter, pkt):
				instrument.packet_count += 1
		
	def AddInstrument(self, chan, name, filter, pattern=None, transpose = 0, vel_dev = 8):
		self.instruments.append(self.Instrument(self.seq, chan, name, filter, pattern, transpose, vel_dev))		

	def DeleteInstrument(self, chan):
		if chan == self.seq.control_channel:
			raise self.seq.DeleteControl(chan)
		else:
			for i in self.instruments:
				if i.chan == chan:
					self.seq.DeleteChannel(chan)
					self.instruments.remove(i)
	
	class Instrument():
		def __init__(self, seq, chan, name, filter, pattern, transpose, vel_dev):
			self.velocity_deviation = vel_dev
			self.transpose = transpose
			self.history_length = 5
			self.chan = chan
			self.name = name
			self.filter = filter
			self.compiled_filter = packetparser.ParseFilter(self.filter)[0]
			self.packet_count = 0
			self.packet_ave = 0
			self.history = []
			self.keynotes = [0, 4, 7]
			seq.AddChannel(chan, name=name)
			self.channel = seq.GetChannel(chan)
			if pattern == None:
				if chan == 10:
					self.channel.pattern = sequencer.DRUM_PATTERN
					self.channel.modable = 0
				else:
					self.channel.pattern = sequencer.BASIC_PATTERN
			else:
				self.channel.pattern = pattern
			print self.chan, self.channel.pattern
			
		@property
		def pattern(self):
			return self.channel.pattern
			
		@property
		def bar_length(self):
			return self.channel.bar_length
			
		@property
		def bar_res(self):
			return self.channel.bar_res

		@property
		def note_length(self):
			return self.channel.note_length
			
		@property
		def modable(self):
			return self.channel.modable
			
		def ResetPacketCount(self):
			self.packet_count = 0
