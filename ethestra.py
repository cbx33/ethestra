from scapy.all import *
import sequencer
import packetparser
import gobject
from threading import Thread
import random
import signal

gobject.threads_init()

fla = 0




def handler(pkt):
    print pkt.summary()
	


class Ethestra():
	def __init__(self):
		gobject.io_add_watch(sys.stdin,
                     gobject.IO_IN | gobject.IO_ERR | gobject.IO_HUP,
                     self.input_handler)
		self.stop_flag = 0
		self.sniffer_thread = Thread(target=self.Start, args=())
		self.sniffer_thread.start()
		self.seq = sequencer.Seq()
		self.seq.SetTempo(100)
		self.seq.AddChannel(1, name="Totoro")
		self.seq.AddChannel(2)
		self.seq.PlayBar()
		self.seq.connect("bar-fin", self.nuts)
		Loop = gobject.MainLoop()
		Loop.run()
		
	def Start(self):
		sniff(prn=handler, filter="ip", store=0, stopper=self.stopperCheck, stopperTimeout=1)

	def input_handler(self, fd, io_condition):
		self.stop_flag = 1
		self.sniffer_thread.join()
		exit(0)
		
	def stopperCheck(self):
		if self.stop_flag:
			return True
		else:
			return False
			
	def nuts(self, e):
		print e.GetChannel(2).pattern
	

ethestra = Ethestra()
