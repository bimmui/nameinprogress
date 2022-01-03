from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.VoltageRatioInput import *
from pathlib import Path
import argparse
import numpy as np
import traceback
import threading, time

BASE_DIR = Path(__file__).resolve()
calibrationweight = None


parser = argparse.ArgumentParser(
    description="nameinprogress")
parser.add_argument("-c",
                    "--calibration",
					choices=['y', 'n'],
                    help="Type 'y' to calibrate before measuring and 'n' to measure using previous calibration factor",
                    type=str, default='n')

args = parser.parse_args()

def countdown(t):
	while t:
		mins, secs = divmod(t, 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		print(timer, end="\r")
		time.sleep(1)
		t -= 1


#Total Loadcell readings class
class Loadcells:
	Mcal = None 
	V1 = 0
	V2 = 0
	V3 = 0
	V4 = 0
	
	calibrationweight = None
	calibrationcomplete = False
	R0_num = None
	def calibrate(self, t, weight, ch0, ch1, ch2, ch3):
		self.calibrationweight = 1
		print('Prepare known weight #1 for measurement')
		background = threading.Thread(target = readsensors, args=(ch0, ch1, ch2, ch3), daemon=True)
		countdown(10)
		background.start()
		print("Now measuring weight #1...")
		countdown(30)


		print("------------------------------")


		print('Prepare known weight #2 for measurement')
		countdown(10)
		self.calibrationweight = 2
		print("Now measuring weight #2...")
		countdown(30)

		self.R0_num = np.average(R0)
		R1_num = np.average(R1)

		Rs = R1_num - self.R0_num
		
		self.Mcal = Rs/weight

		with open('calibrationfactor.txt', 'w') as f:
			f.write("%s \n %s" % (str(self.Mcal), str(self.R0_num)))
		print([str(self.Mcal), str(self.R0_num)])


		loadcellReadings.calibrationcomplete = True
		print('Calibration complete!')

	def getPreviousCalibrationFactoranR0(self):
		with open('calibrationfactor.txt') as f:
			cfr0 = f.readlines()
		self.Mcal = float(cfr0[0])
		self.R0_num = float(cfr0[1])
		loadcellReadings.calibrationcomplete = True

	def totalVoltage(self):
		voltages = [self.V1, self.V2, self.V3, self.V4]
		np_voltages = np.array(voltages)
		return np.sum(np_voltages)

	def totalForce(self):
		voltages = [self.V1, self.V2, self.V3, self.V4]
		np_voltages = np.array(voltages)
		force = (np.sum(np_voltages) - self.R0_num) * self.Mcal
		print("Total force is", force)


  

#object that utilizes the Loadcells class to store voltage inputs, calibration factor, and other class dependent variables
loadcellReadings = Loadcells()

#Declare any event handlers here. These will be called every time the associated event occurs.
def onVoltageRatioChange(self, voltageRatio, loadcellReadings=loadcellReadings):
	if loadcellReadings.calibrationcomplete == True:
		print("VoltageRatio [" + str(self.getChannel()) + "]: " + str(voltageRatio))
		loadcellReadings.totalForce()
	else:
		pass

	if self.getChannel() == 0:
		loadcellReadings.V1 = voltageRatio
	elif self.getChannel() == 1:
		loadcellReadings.V2 = voltageRatio
	elif self.getChannel() == 3:
		loadcellReadings.V3 = voltageRatio
	elif self.getChannel() == 4:
		loadcellReadings.V4 = voltageRatio
	else:
		pass

	if args.calibration == 'y' and loadcellReadings.calibrationcomplete == False:
		if loadcellReadings.calibrationweight == 1:
			R0.append(loadcellReadings.totalVoltage())
		elif loadcellReadings.calibrationweight == 2:
			R1.append(loadcellReadings.totalVoltage())
		else:
			pass
	else:
		pass

def readsensors(ch0, ch1, ch2, ch3):

	#Assign any event handlers you need before calling open so that no events are missed.
	ch0.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	ch0.setOnAttachHandler(onAttach)
	ch0.setOnDetachHandler(onDetach)
	ch0.setOnErrorHandler(onError)
	ch1.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	ch1.setOnAttachHandler(onAttach)
	ch1.setOnDetachHandler(onDetach)
	ch1.setOnErrorHandler(onError)
	ch2.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	ch2.setOnAttachHandler(onAttach)
	ch2.setOnDetachHandler(onDetach)
	ch2.setOnErrorHandler(onError)
	ch3.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	ch3.setOnAttachHandler(onAttach)
	ch3.setOnDetachHandler(onDetach)
	ch3.setOnErrorHandler(onError)

	#Open your Phidgets and wait for attachment
	ch0.openWaitForAttachment(5000)
	ch1.openWaitForAttachment(5000)
	ch2.openWaitForAttachment(5000)
	ch3.openWaitForAttachment(5000)

	#Do stuff with your Phidgets here or in your event handlers.

	try:
		input("Press Enter to Stop. Not recommended when calibrating load cells.\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	ch0.close()
	ch1.close()
	ch2.close()
	ch3.close()


def onAttach(self):
	print("Attach [" + str(self.getChannel()) + "]!")

def onDetach(self):
	print("Detach [" + str(self.getChannel()) + "]!")

def onError(self, code, description):
	print("Code [" + str(self.getChannel()) + "]: " + ErrorEventCode.getName(code))
	print("Description [" + str(self.getChannel()) + "]: " + str(description))
	print("----------")

def main():
	if args.calibration == 'y':
		while True:
			try:
				weight1 = float(input("Please enter your the known weight object #2   "))
			except ValueError:
				print("Sorry, I didn't understand that. I need a number as a valid input.")
				continue
			else:
				break
		global R0
		global R1
		R0 = []
		R1 = []
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

		loadcellReadings.calibrate(30, weight1, voltageRatioInput0, voltageRatioInput1, voltageRatioInput2, voltageRatioInput3)
	else:
		loadcellReadings.getPreviousCalibrationFactoranR0()

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
	try:
		Log.enable(LogLevel.PHIDGET_LOG_INFO, "phidgetlog.log")
		readsensors(voltageRatioInput0, voltageRatioInput1, voltageRatioInput2, voltageRatioInput3)

	except PhidgetException as ex:
		#We will catch Phidget Exceptions here, and print the error informaiton.
		traceback.print_exc()
		print("")
		print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)


main()