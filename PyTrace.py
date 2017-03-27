"""
 * Facilitate execution traceing / logging
 * of execution.
 * For Python based system
 * For Java / Jython systems see BwTrace
 * @author raysm
 *
"""
from __future__ import print_function
from collections import Counter

from PyProperties import PyProperties

BaseTrace = None		# Must be set before any non-trace linked objects are instantiated

def tR(flag, *levels):
	level = 1
	if len(levels) > 0:
		level = 1
	if BaseTrace is not None:
		return BaseTrace.trace(flag, level)
	return True		# Not defined - trace all

class PyTrace(object):
		
	def __init__(self, propFile=None, flagList=None,
			flagStr=None):
		"""
		* Default setup
		flagList - list of flag names to support
				Default level initial setting == 0
				
		flagStr - comma separated list of flag names
			Default (flagList is None and str is None)
			  - "verbose,all,debug"
			  
		propFile - properties file
		"""
		if propFile is None and flagList is None and flagStr is None and BaseTrace is not None:
			return
					
		if propFile is None:
			propFile = "PyTrace.properties"
		self.flagLevel = Counter()
		
		if flagList is None and flagStr is None:
			flagStr = "all,debug,warning,error,verbose" 
		for flag in flagStr.split(","):
			flag = flag.strip()
			self.flagLevel[flag] = 0
			

		# create and load default properties
		self.clearAll()
		prop = self.defaultProps = PyProperties()
		try:
			prop.load(open(propFile))
		except:
			print("Can't find Properties file {}"
				.format(propFile))

		global BaseTrace
		BaseTrace = self		#  Global access
		
		
	def clearAll(self):
		self.setAll(0)

	"""
	 * Set all levels, except debug
	 * @param levels
	"""
	def setAll(self, *vals):
		for flag in dict(self.flagLevel).keys():
			self.setLevel(flag, vals) 

	
	"""
	Set level for flag
	NOTE: one can add new levels, not specified in
		PyTrace constructor call
	"""
	def setLevel(self, trace_name, *vals):
		val = 1
		if len(vals) == 1:
			val = vals[0]
		self.flagLevel[trace_name] = val


	"""
	Set comma separated list of levels to be traced
	NOTE: one can add new levels, not specified in
		PyTrace constructor call
	"""
	def setLevels(self, trace_string, *vals):
		for flag in trace_string.split(","):
			self.setLevel(flag, vals)

	def trace(self, flag, *levels):
		level = 1
		if len(levels) == 1:
			level = levels[0]
		if self.flagLevel[flag] >= level:
			return True
		return False
	
		
	
	def traceInput(self, *levels):
		return self.trace('input', levels)

	
	def traceState(self, *levels):
		return self.trace('state', levels)
	
	def traceDebug(self, *levels):
		return self.trace('debug', levels)

	
	def traceVerbose(self, *levels):
		return self.trace('verbose', levels)
	"""
	 * 
	 * @param key - property key
	 * @return property value, "" if none
	"""
	def getProperty(self, key):
		return self.defaultProps.getProperty(key, "")


	
	def setProperty(self, key, value):
		self.defaultProps.setProperty(key, value)

	"""
	 * Get default properties key with value
	 * stored as comma-separated values
	 * as an array of those values
	 * If propKey not found, return an empty array
	 * @param propKey
	 * @return array of string values
	"""
	def getAsStringArray(self, propKey):
		vals = self.getProperty(propKey).split(",")
		return vals

	"""
	Get flag level
	"""
	def getLevel(self, flag):
		return self.flagLevel[flag]
	
		
	"""
	 * @return the input
	"""
	def getInput(self):
		return self.getLevel('input')


	"""
	 * @return the verbose
	"""
	def getVerbose(self):
		return self.getLevel('verbose')


	"""
	Instance variables
	private Properties defaultProps	// program properties
	private int parse
	private int graphics		// graphics tracing
	private int input
	private int state
	private int execute		// Execution trace
	private int tokenAccept	// If token is accepted
	private int tokenReject	// If token is rejected
	private int token
	private int mark
	private int accept
	private int backup
	private int debug			// DEBUG setting - temporary use
	private int tokStack
	private int tokQueue
	"""

    
if __name__=="__main__":
	flagStr="input,output,throughput,shotput"	
	traceObj = PyTrace(flagStr)
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

		
		
		
		
