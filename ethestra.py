from scapy.all import *
import sequencer
import gobject
from threading import Thread
import random
import signal

gobject.threads_init()

fla = 0

seq = sequencer.Seq()
seq.SetTempo(100)

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


	
def nuts(e):
	print e.GetChannel(2).pattern

#sniff(prn=handler, filter="ip", store=0)
#sniff(prn=handler, store=0)
seq.AddChannel(1, name="Totoro")
seq.AddChannel(2)
seq.PlayBar()
seq.connect("bar-fin", nuts)

def stopperCheck():
	global fla
	if fla:
		return True
	else:
		return False

def blarg(yikes):
		sniff(prn=handler, filter="ip", store=0, stopper=stopperCheck, stopperTimeout=1)

t = Thread(target=blarg, args=("o",))
t.start()

def input_handler(fd, io_condition):
	global fla
	fla = 1
	t.join()
	exit(0)

gobject.io_add_watch(sys.stdin,
                     gobject.IO_IN | gobject.IO_ERR | gobject.IO_HUP,
                     input_handler)

Loop = gobject.MainLoop()

Loop.run()
