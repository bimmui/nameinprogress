from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.VoltageRatioInput import *
import numpy as np
import traceback
import time

#Total voltage class
class totalVoltage:
	V1 = 0
	V2 = 0
	V3 = 0
	V4 = 0

	def totalVoltageGetter(self):
		voltages = [self.V1, self.V2, self.V3, self.V4]
		print("Total voltage is", np.sum(voltages))

#Total voltage variable that utilizes the totalVoltage class to store voltage inputs
totalVoltageRatio = totalVoltage()

#Declare any event handlers here. These will be called every time the associated event occurs.
def onVoltageRatioChange(self, voltageRatio, totalVoltageRatio=totalVoltageRatio):
	print("VoltageRatio [" + str(self.getChannel()) + "]: " + str(voltageRatio))
	if self.getChannel() == 0:
		totalVoltageRatio.V1 = voltageRatio
	elif self.getChannel() == 1:
		totalVoltageRatio.V2 = voltageRatio
	elif self.getChannel() == 3:
		totalVoltageRatio.V3 = voltageRatio
	elif self.getChannel() == 4:
		totalVoltageRatio.V4 = voltageRatio
	else:
		pass

	print(totalVoltageRatio.totalVoltageGetter())

def onAttach(self):
	print("Attach [" + str(self.getChannel()) + "]!")

def onDetach(self):
	print("Detach [" + str(self.getChannel()) + "]!")

def onError(self, code, description):
	print("Code [" + str(self.getChannel()) + "]: " + ErrorEventCode.getName(code))
	print("Description [" + str(self.getChannel()) + "]: " + str(description))
	print("----------")

def main():
	try:
		Log.enable(LogLevel.PHIDGET_LOG_INFO, "phidgetlog.log")
		#Create your Phidget channels
		voltageRatioInput0 = VoltageRatioInput()
		voltageRatioInput1 = VoltageRatioInput()
		voltageRatioInput2 = VoltageRatioInput()
		voltageRatioInput3 = VoltageRatioInput()

		#Set addressing parameters to specify which channel to open (if any)
		voltageRatioInput0.setChannel(0)
		voltageRatioInput1.setChannel(1)
		voltageRatioInput2.setChannel(2)
		voltageRatioInput3.setChannel(3)

		#Assign any event handlers you need before calling open so that no events are missed.
		voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
		voltageRatioInput0.setOnAttachHandler(onAttach)
		voltageRatioInput0.setOnDetachHandler(onDetach)
		voltageRatioInput0.setOnErrorHandler(onError)
		voltageRatioInput1.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
		voltageRatioInput1.setOnAttachHandler(onAttach)
		voltageRatioInput1.setOnDetachHandler(onDetach)
		voltageRatioInput1.setOnErrorHandler(onError)
		voltageRatioInput2.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
		voltageRatioInput2.setOnAttachHandler(onAttach)
		voltageRatioInput2.setOnDetachHandler(onDetach)
		voltageRatioInput2.setOnErrorHandler(onError)
		voltageRatioInput3.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
		voltageRatioInput3.setOnAttachHandler(onAttach)
		voltageRatioInput3.setOnDetachHandler(onDetach)
		voltageRatioInput3.setOnErrorHandler(onError)

		#Open your Phidgets and wait for attachment
		voltageRatioInput0.openWaitForAttachment(5000)
		voltageRatioInput1.openWaitForAttachment(5000)
		voltageRatioInput2.openWaitForAttachment(5000)
		voltageRatioInput3.openWaitForAttachment(5000)

		#Do stuff with your Phidgets here or in your event handlers.

		try:
			input("Press Enter to Stop\n")
		except (Exception, KeyboardInterrupt):
			pass

		#Close your Phidgets once the program is done.
		voltageRatioInput0.close()
		voltageRatioInput1.close()
		voltageRatioInput2.close()
		voltageRatioInput3.close()

	except PhidgetException as ex:
		#We will catch Phidget Exceptions here, and print the error informaiton.
		traceback.print_exc()
		print("")
		print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)


main()