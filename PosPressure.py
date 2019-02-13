
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
import PyCapture2


# def camera(nFrames, save_dir):
#
# 	def capIm():
# 		# Function retreives buffer from FLIR camera in place of cv2 capture
# 		try:
# 			img = cam.retrieveBuffer()
# 		except PyCapture2.Fc2error as fc2Err:
# 			print("Error retrieving buffer :", fc2Err)
# 			return False, []
#
# 		data = np.asarray(img.getData(), dtype=np.uint8)
# 		data = data.reshape((img.getRows(), img.getCols()))
#
# 		return True, data
#
#
# 	bus = PyCapture2.BusManager()
# 	cam = PyCapture2.Camera()
# 	uid = bus.getCameraFromIndex(0)
# 	cam.connect(uid)
# 	cam.startCapture()
#
# 	photos = []
#
# 	t0 = time.time()
#
# 	for i in range(nFrames):
#
# 		ret = True
# 		ret, frame = capIm()
# 		frame = np.expand_dims(frame, 2)
# 		frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
#
# 		cv2.imshow("Frame", frame)
# 		photos.append(frame)
#
# 		print((i+1)/(time.time() - t0))
#
# 		# Video keyboard interrupt
# 		if cv2.waitKey(1) & 0xFF == ord('q'):
# 			break
#
#
# 	with open(save_dir+'/photos.pkl', 'wb') as f:
# 		pickle.dump(photos, f)
#
#
# 	cam.stopCapture()
# 	cam.disconnect()
# 	cv2.destroyAllWindows()
# 	cv2.waitKey()
#
def pneumaticsAndLights(ser, times, odor, switched):

	ser.write(str.encode('1'))
	time.sleep(t1)
	ser.write(str.encode('3'))
	time.sleep(t2)
	ser.write(str.encode('1'))
	time.sleep(t3)
	ser.write(str.encode('2'))


#========================================================================================================

def run(comm, baud, blockList, nTrials, outFolder):


	dt = datetime.now()
	datetimeString = str(dt.month)+"_"+str(dt.day)+"_"+str(dt.year)+"_"+str(dt.hour)+str(dt.minute)

	ser = serial.Serial(comm, baud)
	time.sleep(2)

	# Set Flow Rate
	#ser.write(FLOW RATE ANALOG OUTPUTS)


	timeList = [float(block.duration) for block in blockList]
	cfgList = [getCfg(block) for block in blockList]


	for i in range(nTrials):
		print("Trial {}".format(i))
		saveDir = outFolder + datetimeString + '/Trial{}'.format(i)

		os.makedirs(save_dir)

		pneumaticsAndLightsThread = threading.Thread(target = pneumaticsAndLights, args=(ser, ))
		cameraThread = threading.Thread(target = camera, args=(nFrames, save_dir,))

		pneumaticsAndLightsThread.start()
		cameraThread.start()
	#
	#
	# 	#while (pneumatics_thread.isAlive()) or (camera_thread.isAlive()):
	# 	while (camera_thread.isAlive()):
	# 		time.sleep(0.1)
	# 	time.sleep(5)
	#
	# print("Processing Pickles")
	#
	# list_of_folders = os.listdir(out_folder + datetime_string)
	#
	#
	# for folder in list_of_folders:
	# 	with open(out_folder + datetime_string+'/'+folder+'/photos.pkl', 'rb') as f:
	# 		photos = pickle.load(f)
	#
	# 		for i, photo in enumerate(photos):
	# 			frame = np.expand_dims(photo, 2)
	# 			cl_frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
	# 			#bw_frame = cv2.cvtColor(cl_frame, cv2.COLOR_BGR2GRAY)
	#
	# 			cv2.imwrite(out_folder + datetime_string+'/'+folder+"/{}.jpg".format(i), cl_frame)
	#
	# 	os.remove(out_folder + datetime_string+'/'+folder+'/photos.pkl')
