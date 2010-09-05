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
                     self.InputHandler)
		self.stop_flag = 0
		self.sniffer_thread = Thread(target=self.StartSniffer, args=())
		self.sniffer_thread.start()
		self.seq = sequencer.Seq()
		self.seq.SetTempo(100)
		self.seq.AddChannel(1, name="Totoro")
		self.seq.AddChannel(2)
		self.seq.PlayBar()
		self.seq.connect("bar-fin", self.FinishedBar)
		Loop = gobject.MainLoop()
		Loop.run()
		
	def StartSniffer(self):
		sniff(prn=handler, filter="ip", store=0, stopper=self.StopperCheck, stopperTimeout=1)

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
		print e.GetChannel(2).pattern
	

ethestra = Ethestra()
