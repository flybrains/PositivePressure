
import  numpy as np
import cv2
import sys
import time
from os import system
import os
import pickle
import threading
from datetime import datetime
import serial

#import PyCapture2

class Block(object):
	def __init__(self, duration, lightConfig, flowDir, flowGas):
		self.duration = duration
		self.lightConfig = lightConfig
		self.flowDir = flowDir
		self.flowGas = flowGas

def getCfg(block):

	lc = block.lightConfig
	fd = block.flowDir
	fg = block.flowGas

	if (lc==0) and (fd==1) and (fg==1):
		returnVal = b'1'
	if (lc==0) and (fd==2) and (fg==1):
		returnVal = '2'
	if (lc==0) and (fd==1) and (fg==2):
		returnVal = b'3'
	if (lc==0) and (fd==2) and (fg==2):
		returnVal = '4'
	if (lc==0) and (fg==0):
		returnVal = '5'

	if (lc==1) and (fd==1) and (fg==1):
		returnVal = '6'
	if (lc==1) and (fd==2) and (fg==1):
		returnVal = '7'
	if (lc==1) and (fd==1) and (fg==2):
		returnVal = '8'
	if (lc==1) and (fd==2) and (fg==2):
		returnVal = '9'
	if (lc==1) and (fg==0):
		returnVal = 'a'

	if (lc==2) and (fd==1) and (fg==1):
		returnVal = 'b'
	if (lc==2) and (fd==2) and (fg==1):
		returnVal = 'c'
	if (lc==2) and (fd==1) and (fg==2):
		returnVal = 'd'
	if (lc==2) and (fd==2) and (fg==2):
		returnVal = 'e'
	if (lc==2) and (fg==0):
		returnVal = 'f'

	if (lc==3) and (fd==1) and (fg==1):
		returnVal = 'g'
	if (lc==3) and (fd==2) and (fg==1):
		returnVal = 'h'
	if (lc==3) and (fd==1) and (fg==2):
		returnVal = 'i'
	if (lc==3) and (fd==2) and (fg==2):
		returnVal = 'j'
	if (lc==3) and (fg==0):
		returnVal = 'k'

	if (lc==4) and (fd==1) and (fg==1):
		returnVal = 'l'
	if (lc==4) and (fd==2) and (fg==1):
		returnVal = 'm'
	if (lc==4) and (fd==1) and (fg==2):
		returnVal = 'n'
	if (lc==4) and (fd==2) and (fg==2):
		returnVal = 'o'
	if (lc==4) and (fg==0):
		returnVal = 'p'
	return returnVal



def camera(nFrames, save_dir):

	def capIm():
	# Function retreives buffer from FLIR camera in place of cv2 capture
		try:
			img = cam.retrieveBuffer()
		except PyCapture2.Fc2error as fc2Err:
			print("Error retrieving buffer :", fc2Err)
		return False, []

	data = np.asarray(img.getData(), dtype=np.uint8)
	data = data.reshape((img.getRows(), img.getCols()))

	return True, data

	bus = PyCapture2.BusManager()
	cam = PyCapture2.Camera()
	uid = bus.getCameraFromIndex(0)
	cam.connect(uid)
	cam.startCapture()

	photos = []

	t0 = time.time()

	for i in range(nFrames):
		ret = True
		ret, frame = capIm()
		frame = np.expand_dims(frame, 2)
		frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)

		cv2.imshow("Frame", frame)
		photos.append(frame)

		print((i+1)/(time.time() - t0))

		# Video keyboard interrupt
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


	with open(save_dir+'/photos.pkl', 'wb') as f:
		pickle.dump(photos, f)

	cam.stopCapture()
	cam.disconnect()
	cv2.destroyAllWindows()
	cv2.waitKey()

def pneumaticsAndLights(ser, programLists):

	timeList = programLists[0]
	cfgList = programLists[1]

	for index in range(len(cfgList)):
		ser.write(str.encode(cfgList[index]))
		time.sleep(timeList[index])




#========================================================================================================

def run(comm, baud, blockList, nTrials, outFolder):

	dt = datetime.now()
	datetimeString = str(dt.month)+"_"+str(dt.day)+"_"+str(dt.year)+"_"+str(dt.hour)+str(dt.minute)

	betweenTrialSleepTime = 15

	ser = serial.Serial(comm, baud)
	time.sleep(2)

	timeList = [float(block.duration) for block in blockList]
	cfgList = [getCfg(block) for block in blockList]
	programLists = [timeList, cfgList]

	timeSum = np.sum(timeList)
	nFrames = int(timeSum*30)

	for i in range(nTrials):
		print("Trial {}".format(i))
		saveDir = outFolder + datetimeString + '/Trial{}'.format(i)
		#os.makedirs(saveDir)

		pneumaticsAndLightsThread = threading.Thread(target = pneumaticsAndLights, args=(ser, programLists, ))
		cameraThread = threading.Thread(target = camera, args=(nFrames, saveDir,))

		pneumaticsAndLightsThread.start()
		#cameraThread.start()

		while (pneumaticsAndLightsThread.isAlive()):# or (cameraThread.isAlive()):
		# 	while (cameraThread.isAlive()):
			time.sleep(0.1)
		time.sleep(betweenTrialSleepTime)

	print("Processing Pickles")

	# list_of_folders = os.listdir(outFolder + datetimeString)
	#
	#
	# for folder in list_of_folders:
	# 	with open(outFolder + datetimeString+'/'+folder+'/photos.pkl', 'rb') as f:
	# 		photos = pickle.load(f)
	#
	# 		for i, photo in enumerate(photos):
	# 			frame = np.expand_dims(photo, 2)
	# 			cl_frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
	# 			#bw_frame = cv2.cvtColor(cl_frame, cv2.COLOR_BGR2GRAY)
	#
	# 			cv2.imwrite(outFolder + datetimeString+'/'+folder+"/{}.jpg".format(i), cl_frame)
	#
	# 	os.remove(outFolder + datetimeString+'/'+folder+'/photos.pkl')
