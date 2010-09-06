from scapy.all import *
import sequencer
import packetparser
import gobject
from threading import Thread
import random
import signal

gobject.threads_init()
	
DISABLE_SNIFFER = 0
	
class Ethestra():
	def __init__(self, device_name, channels_to_add, tempo = 100):
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
		#print e.GetChannel(1).pattern
		#print e.GetChannel(2).pattern
		for instrument in self.instruments:
			print instrument.chan, instrument.name, instrument.packet_count
		
	def PacketHandler(self, pkt):
		print pkt.summary()
		for instrument in self.instruments:
			if packetparser.FilterCheck(instrument.compiled_filter, pkt):
				instrument.packet_count += 1
		
	def AddInstrument(self, chan, name, filter):
		self.instruments.append(self.Instrument(self.seq, chan, name, filter))		
	
	class Instrument():
		def __init__(self, seq, chan, name, filter):
			self.chan = chan
			self.name = name
			self.filter = filter
			self.compiled_filter = packetparser.ParseFilter(self.filter)[0]
			self.packet_count = 0
			print self.compiled_filter
			seq.AddChannel(chan, name=name)
			
channels_to_add = [
(1, "ARP Instrument", "IS ARP"),
(2, "TCP Instrument", "IS TCP"),]
ethestra = Ethestra("ZynAddSubFX", channels_to_add, tempo=100)
