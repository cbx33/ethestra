from scapy.all import *
import sequencer
import packetparser
import gobject
from threading import Thread
import random
import signal
import quantization as qtz

DISABLE_SNIFFER = 0
	
class Ethestra():
	def __init__(self, device_name, channels_to_add, tempo = 100):
		gobject.threads_init()
		gobject.io_add_watch(sys.stdin,
                     gobject.IO_IN | gobject.IO_ERR | gobject.IO_HUP,
                     self.InputHandler)
		self.stop_flag = 0
		self.seq = sequencer.Seq(device_name)
		self.seq.SetTempo(tempo)
		self.instruments = []
		for channel in channels_to_add:
			print channel
			self.AddInstrument(channel[0], channel[1], channel[2])
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
			#print instrument.chan, instrument.name, instrument.packet_count, instrument.channel.pattern
			instrument.history.append(instrument.packet_count)
			if len(instrument.history) > instrument.history_length:
				instrument.history.pop(0)
			instrument.packet_ave = sum(instrument.history) / instrument.history_length
			instrument.ResetPacketCount()
			print instrument.history, instrument.packet_ave
		
	def PacketHandler(self, pkt):
		print pkt.summary()
		for instrument in self.instruments:
			if packetparser.FilterCheck(instrument.compiled_filter, pkt):
				#~ note_position = qtz.ReturnNotePosition(bar_length = instrument.channel.bar_length, bar_res = instrument.channel.bar_res)
				#~ instrument.channel.pattern.append((note_position, 0x50, 0x60, 4))
				instrument.packet_count += 1
		
	def AddInstrument(self, chan, name, filter):
		self.instruments.append(self.Instrument(self.seq, chan, name, filter))		
	
	class Instrument():
		def __init__(self, seq, chan, name, filter):
			self.history_length = 5
			self.chan = chan
			self.name = name
			self.filter = filter
			self.compiled_filter = packetparser.ParseFilter(self.filter)[0]
			self.packet_count = 0
			self.packet_ave = 0
			self.history = []
			seq.AddChannel(chan, name=name)
			self.channel = seq.GetChannel(chan)
			if chan == 10:
				self.channel.pattern = sequencer.DRUM_PATTERN
			else:
				self.channel.pattern = sequencer.BASIC_PATTERN
			print self.chan, self.channel.pattern
			
		def ResetPacketCount(self):
			self.packet_count = 0
