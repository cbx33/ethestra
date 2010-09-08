import core

#TODO
# Add trigger filters which make drastic change, such as reorder instruments
#	and have a defined cool-off period to prevent multiple activations
# Add Drum Channel handling
# Make ReturnNote deploy note pitch too

ethestra = core.Ethestra("ZynAddSubFX", tempo=100)
ethestra.AddInstrument(1, "ARP Instrument", "IS ARP", pattern=None)
ethestra.AddInstrument(2, "ARP Instrument", "IS ARP OR IS TCP", pattern=[])
ethestra.AddInstrument(10, "ARP Instrument", "IS TCP", pattern=None)
ethestra.Start()
