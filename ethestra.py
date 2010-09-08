import core

#TODO
# Add trigger filters which make drastic change, such as reorder instruments
#	and have a defined cool-off period to prevent multiple activations
# Add Drum Channel handling
# Make ReturnNote deploy note pitch too

channels_to_add = [
(1, "ARP Instrument", "IS ARP"),
(2, "TCP Instrument", "IS TCP"),
(10, "TCP Instrument", "IS TCP"),]
ethestra = core.Ethestra("ZynAddSubFX", channels_to_add, tempo=100)
