from scapy.all import *
import sequencer
import packetparser
import gobject
from threading import Thread
import random
import signal

gobject.threads_init()

fla = 0



ch1 = 0
ch2 = 0
ch3 = 0
ch4 = 0
ch5 = 0
ch12 = 0
mod1 = 0
mod2 = 0
mod3 = 0
mod4 = 0
mod5 = 0
mod12 = 0

def handler(pkt):
    print pkt.summary()
    """
    #print pkt.type
    global seq
    
    global arg
    global ch1, ch2, ch3, ch4, ch5, ch12
    global mod1, mod2, mod3, mod4, mod5, mod12

    if LLC in pkt:
		return
	
    if pkt.type != 2048:
		return

    if pkt.proto == 6 or pkt.proto == 17:
	    if pkt.dport == 5222 or pkt.sport == 5222:
		print "CHAT"
		seq.GetChannel(2).pattern.append([random.random()*64, 0x2A, 0x60, 4])
	"""

	
def nuts(e):
	print e.GetChannel(2).pattern




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
		self.seq.connect("bar-fin", nuts)
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
	

ethestra = Ethestra()
