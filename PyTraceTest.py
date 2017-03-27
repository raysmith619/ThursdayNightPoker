"""
 * Separate file test of PyTrace
 * @author raysm
 *
"""
from __future__ import print_function

import PyTrace

flagStr="input,output,throughput,shotput"	
traceObj = PyTrace.PyTrace(flagStr)
traceObj.setLevel('input',1)
traceObj.setLevel('output')
traceObj.setLevel('shotput', 2)
traceObj.setLevels("one,three")
#traceObj.setLevel('throughput')

if traceObj.trace('input'):
	print("input is set")
else:
	print("input is NOT set")

if traceObj.trace('output'):
	print("output is set")
else:
	print("output is NOT set")

if traceObj.trace('throughput'):
	print("throughput is set")
else:
	print("throughput is NOT set")

if traceObj.trace('shotput'):
	print("shotput is set")
else:
	print("shotput is NOT set")

if traceObj.trace('shotput', 2):
	print("shotput 2 is set")
else:
	print("shotput 2 is NOT set")

if traceObj.trace('shotput', 3):
	print("shotput 3 is set")
else:
	print("shotput 3 is NOT set")
	

if traceObj.trace('one'):
	print("one is set")
else:
	print("one is NOT set")

if traceObj.trace('two'):
	print("two is set")
else:
	print("two is NOT set")

if traceObj.trace('three'):
	print("three is set")
else:
	print("three is NOT set")

print("\nUsing tR static funcgtion")
from PyTrace import tR
if tR('input'):
	print("input is set")
else:
	print("input is NOT set")

if tR('output'):
	print("output is set")
else:
	print("output is NOT set")

if tR('throughput'):
	print("throughput is set")
else:
	print("throughput is NOT set")

if tR('shotput'):
	print("shotput is set")
else:
	print("shotput is NOT set")

if tR('shotput', 2):
	print("shotput 2 is set")
else:
	print("shotput 2 is NOT set")

if tR('shotput', 3):
	print("shotput 3 is set")
else:
	print("shotput 3 is NOT set")
	

if tR('one'):
	print("one is set")
else:
	print("one is NOT set")

if tR('two'):
	print("two is set")
else:
	print("two is NOT set")

if tR('three'):
	print("three is set")
else:
	print("three is NOT set")

		
		
		
		
