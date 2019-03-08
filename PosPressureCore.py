
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

import flycapture2 as fc2

class Block(object):
	def __init__(self, duration, lightConfig, flowDir, flowGas, 
				recording, pairing, lightDspTxt, fgString, recString, pairString):
		self.duration = duration
		self.lightConfig = lightConfig
		self.flowDir = flowDir
		self.flowGas = flowGas
		self.recording = recording
		self.pairing = pairing

		self.lightDspTxt = lightDspTxt
		self.fgString = fgString
		self.recString = recString
		self.pairString = pairString


	def addFN(self, FN):
		self.folderName = FN

		return None


def getCfg(block):

	lc = block.lightConfig
	fd = block.flowDir
	fg = block.flowGas

	if (lc==0) and (fd==1) and (fg==1):
		returnVal = '1'
	if (lc==0) and (fd==2) and (fg==1):
		returnVal = '2'
	if (lc==0) and (fd==1) and (fg==2):
		returnVal = '3'
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

def reverseCfg(IDString):

	if IDString == '1':
		returnVal = 'No Light\tDirection 1\tAir'
	if IDString == '2':
		returnVal = 'No Light\tDirection 2\tAir'
	if IDString == '3':
		returnVal = 'No Light\tDirection 1\tOdor'
	if IDString == '4':
		returnVal = 'No Light\tDirection 2\tOdor'
	if IDString == '5':
		returnVal = 'No Light\tNo Flow'

	if IDString == '6':
		returnVal = 'Low Green\tDirection 1\tAir'
	if IDString == '7':
		returnVal = 'Low Green\tDirection 2\tAir'
	if IDString == '8':
		returnVal = 'Low Green\tDirection 1\tOdor'
	if IDString == '9':
		returnVal = 'Low Green\tDirection 2\tOdor'
	if IDString == 'a':
		returnVal = 'Low Green\tNo Flow'


	if IDString == 'b':
		returnVal = 'High Green\tDirection 1\tAir'
	if IDString == 'c':
		returnVal = 'High Green\tDirection 2\tAir'
	if IDString == 'd':
		returnVal = 'High Green\tDirection 1\tOdor'
	if IDString == 'e':
		returnVal = 'High Green\tDirection 2\tOdor'
	if IDString == 'f':
		returnVal = 'High Green\tNo Flow'

	if IDString == 'g':
		returnVal = 'Low Red\tDirection 1\tAir'
	if IDString == 'h':
		returnVal = 'Low Red\tDirection 2\tAir'
	if IDString == 'i':
		returnVal = 'Low Red\tDirection 1\tOdor'
	if IDString == 'j':
		returnVal = 'Low Red\tDirection 2\tOdor'
	if IDString == 'k':
		returnVal = 'Low Red\tNo Flow'

	if IDString == 'l':
		returnVal = 'High Red\tDirection 1\tAir'
	if IDString == 'm':
		returnVal = 'High Red\tDirection 2\tAir'
	if IDString == 'n':
		returnVal = 'High Red\tDirection 1\tOdor'
	if IDString == 'o':
		returnVal = 'High Red\tDirection 2\tOdor'
	if IDString == 'p':
		returnVal = 'High Red\tNo Flow'
	return returnVal

# def camera(nFrames, save_dir):

# 	def capIm():
# 	# Function retreives buffer from FLIR camera in place of cv2 capture
# 		try:
# 			img = cam.retrieveBuffer()
# 		except PyCapture2.Fc2error as fc2Err:
# 			print("Error retrieving buffer :", fc2Err)
# 		return False, []

# 	data = np.asarray(img.getData(), dtype=np.uint8)
# 	data = data.reshape((img.getRows(), img.getCols()))

# 	return True, data

# 	bus = PyCapture2.BusManager()
# 	cam = PyCapture2.Camera()
# 	uid = bus.getCameraFromIndex(0)
# 	cam.connect(uid)
# 	cam.startCapture()

# 	photos = []

# 	t0 = time.time()

# 	for i in range(nFrames):
# 		ret = True
# 		ret, frame = capIm()
# 		frame = np.expand_dims(frame, 2)
# 		frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)

# 		cv2.imshow("Frame", frame)
# 		photos.append(frame)

# 		print((i+1)/(time.time() - t0))

# 		# Video keyboard interrupt
# 		if cv2.waitKey(1) & 0xFF == ord('q'):
# 			break


# 	with open(save_dir+'/photos.pkl', 'wb') as f:
# 		pickle.dump(photos, f)

# 	cam.stopCapture()
# 	cam.disconnect()
# 	cv2.destroyAllWindows()
# 	cv2.waitKey()

def camera(n_frames, save_dir):

	cap = fc2.Context()
	cap.connect(*cap.get_camera_from_index(0))
	cap.set_video_mode_and_frame_rate(fc2.VIDEOMODE_640x480Y8, fc2.FRAMERATE_30)
	m, f = cap.get_video_mode_and_frame_rate()
	p = cap.get_property(fc2.FRAME_RATE)
	cap.set_property(**p)
	cap.start_capture()

	photos = []

	baseTime = time.time()

	for i in range(n_frames):

		img = fc2.Image()
		cap.retrieve_buffer(img)
		frame = np.array(img)

		#cv2.imshow("Frame", frame)
		photos.append(frame)

		# Video keyboard interrupt
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	#print('Photo Set of {} Done at : {}'.format(n_frames, (time.time() - baseTime)))

	if save_dir is not None:
		with open(save_dir+'/photos.pkl', 'wb') as f:
			pickle.dump(photos, f)
	else:
		pass


	cap.stop_capture()
	cap.disconnect()
	cv2.destroyAllWindows()
	cv2.waitKey()

def pneumaticsAndLights(ser, programLists, wrap):

	timeList = programLists[0]
	cfgList = programLists[1]

	for index in range(len(cfgList)):

		c = str(cfgList[index])
		print(reverseCfg(c))

		ser.write(str.encode(cfgList[index]))
		#ser.write(cfgList[index])
		time.sleep(timeList[index])

	if wrap==True:
		ser.write(str.encode('0'))
	else:
		pass

#========================================================================================================

def run(comm, baud, blockList, outFolder):

	# Do dummy camera thread with one frame and no recording to speed context creation later
	cameraThread = threading.Thread(target = camera, args=(1, None,))
	cameraThread.start()

	dt = datetime.now()
	datetimeString = str(dt.month)+"_"+str(dt.day)+"_"+str(dt.year)+"_"+str(dt.hour)+str(dt.minute)

	ser = serial.Serial(comm, baud)
	time.sleep(2)

	segments = []
	newSeg = []
	

	for idx, block in enumerate(blockList):
		if idx==0:
			newSeg = [block]
			lastBlockFN = block.folderName
		
		if (idx>0) and (lastBlockFN==block.folderName):
			newSeg.append(block)
			lastBlockFN = block.folderName

		if (lastBlockFN!=block.folderName):
			segments.append(newSeg)
			newSeg = []
			newSeg.append(block)
			lastBlockFN = block.folderName

		if (idx == len(blockList)-1):
			segments.append(newSeg)


	for idx, segment in enumerate(segments):

		timeList = [float(block.duration) for block in segment]
		cfgList = [getCfg(block) for block in segment]
		programLists = [timeList, cfgList]

		timeSum = np.sum(timeList)
		nFrames = int(timeSum*30)

		if idx==(len(segments)-1):
			wrap = True
		else:
			wrap = False


		if segment[0].recording==True:

			saveDir = outFolder + "/"+datetimeString + '/{}'.format(segment[0].folderName)
			os.makedirs(saveDir)

			pneumaticsAndLightsThread = threading.Thread(target = pneumaticsAndLights, args=(ser, programLists, wrap, ))
			cameraThread = threading.Thread(target = camera, args=(nFrames, saveDir,))

			pneumaticsAndLightsThread.start()
			cameraThread.start()

			while (pneumaticsAndLightsThread.isAlive() or cameraThread.isAlive()):
				time.sleep(0.1)

		else:
			pneumaticsAndLightsThread = threading.Thread(target = pneumaticsAndLights, args=(ser, programLists, wrap, ))
			pneumaticsAndLightsThread.start()

			while (pneumaticsAndLightsThread.isAlive()):
				time.sleep(0.01)

	

	list_of_folders = os.listdir(outFolder +"/"+datetimeString)
	
	
	for idx, folder in enumerate(list_of_folders):
		print("Processing Pickles {} / {}".format(idx+1, len(list_of_folders)))
		with open(outFolder +'/'+datetimeString+'/'+folder+'/photos.pkl', 'rb') as f:
			photos = pickle.load(f)
	
			for i, photo in enumerate(photos):
				frame = np.expand_dims(photo, 2)
				cl_frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
				#bw_frame = cv2.cvtColor(cl_frame, cv2.COLOR_BGR2GRAY)
	
				cv2.imwrite(outFolder +'/'+ datetimeString+'/'+folder+"/{}.tiff".format(i), cl_frame)
	
		os.remove(outFolder +'/'+datetimeString+'/'+folder+'/photos.pkl')
	print('Done')
