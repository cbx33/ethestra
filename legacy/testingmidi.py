from scapy.all import *

import portmidizero
import time

CHORD=40
OUTPUT = 1
INPUT = 0

def OpenDevice ():
    """ """
    for loop in range(portmidizero.CountDevices()):
        interf,name,inp,outp,opened = portmidizero.GetDeviceInfo(loop)
        print name
        if outp == 1 and name == "ZynAddSubFX":
           print "OK %s" % name
           return portmidizero.Output(loop,0)

def PrintDevices(InOrOut):
    for loop in range(portmidizero.CountDevices()):
        interf,name,inp,outp,opened = portmidizero.GetDeviceInfo(loop)
        if ((InOrOut == INPUT) & (inp == 1) |
            (InOrOut == OUTPUT) & (outp ==1)):
            print loop, name," ",
            if (inp == 1): print "(input) ",
            else: print "(output) ",
            if (opened == 1): print "(opened)"
            else: print "(unopened)"
    print

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

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
    global arg
    global ch1, ch2, ch3, ch4, ch5, ch12
    global mod1, mod2, mod3, mod4, mod5, mod12

    if LLC in pkt:
	return

    if ARP in pkt:
		if ch3 == 0:
		    if mod3 == 0:
			mod3 = 3
		    elif mod3 == 3:
		        mod3 = 7
		    else:
			mod3 = 0
		    arg.WriteShort(0x90+2,0x50+mod3,0x60)
		    ch3 = 1
	    	else: 
		    arg.WriteShort(0x80+2,0x50+mod3,0x60)
		    ch3 = 0
		return
    if ICMP in pkt:
		if ch4 == 0:
		    if mod4 == 0:
			mod4 = 3
		    elif mod4 == 3:
		        mod4 = 7
		    else:
			mod4 = 0
		    arg.WriteShort(0x90+9,0x30,0x65)
		    ch4 = 1
	    	else: 
		    arg.WriteShort(0x80+9,0x30,0x65)
		    ch4 = 0
		return

    if pkt.type != 2048:
		return

    if pkt.proto == 6 or pkt.proto == 17:
	    if pkt.dport == 5222 or pkt.sport == 5222:
		if ch5 == 0:
		    if mod5 == 0:
			mod5 = 3
		    elif mod5 == 3:
		        mod5 = 7
		    else:
			mod5 = 0
		    arg.WriteShort(0x90+3,0x50+mod5,0x30)
		    ch5 = 1
	    	else: 
		    arg.WriteShort(0x80+3,0x50+mod5,0x30)
		    ch5 = 0


	    if pkt.dport == 80:
		if ch1 == 0:
		    if mod1 == 0:
			mod1 = 3
		    elif mod1 == 3:
		        mod1 = 7
		    else:
			mod1 = 0
		    arg.WriteShort(0x90+1,0x50+mod1,0x60)
		    ch1 = 1
	    	else: 
		    arg.WriteShort(0x80+1,0x50+mod1,0x60)
		    ch1 = 0
	    if pkt.dport == 443:
		if ch12 == 0:
		    if mod12 == 0:
			mod12 = 3
		    elif mod12 == 3:
		        mod12 = 7
		    else:
			mod12 = 0
		    arg.WriteShort(0x90+1,0x50+mod12-24,0x40)
		    ch12 = 1
	    	else: 
		    arg.WriteShort(0x80+1,0x50+mod12-24,0x40)
		    ch12 = 0
	    if pkt.dport == 53 or pkt.sport == 53:
		if ch2 == 0:
		    if mod2 == 0:
			mod2 = 3
		    elif mod2 == 3:
		        mod2 = 7
		    else:
			mod2 = 0
		    arg.WriteShort(0x90,0x50+mod2-36,0x60)
		    ch2 = 1
	    	else: 
		    arg.WriteShort(0x80,0x50+mod2-36,0x60)
		    ch2 = 0
	    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
		return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")



arg = OpenDevice()
PrintDevices(1)

arg.WriteShort(0x90,0x50+3,0x60)
time.sleep(0.1)
arg.WriteShort(0x80,0x50+3,0x60)


#sniff(prn=handler, filter="tcp", store=0, count = 20)
sniff(prn=handler, store=0)


del arg
arg = None
pass

PrintDevices(1)

#1 Ahh Choir 1		69 system
#2 Arpeggio 1
#3 Space Voice1
#4 Impossible Dream2   75 system
#10 Drums Kit1		92 system

#System Very long Reverb

#CLEANUP
#MAP TCP HANDSHAKE
