#               PROJECT - Video Analysis
#    Press SPACE to capture frame 
#
#    Press 'P' to pause video. To resume press any key
#    Press 'F' to make video faster
#    Press 'S' to make video go slower
#    Press 'R' to clear Histograms window
#
#    Willie - week 2 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np
import random as rd

debugging = True   # Boolean variable for debugging

bins = np.arange(256).reshape(256,1)

usage = '''
USAGE:      SPACE - capture frame

            'P' - to pause. To resume press any key

            'F' - makes video run faster

            'S' - makes video run slower

            'R' - clears Histograms window

     QUIT: press either q or ESC
'''

def getHistogram(img):

	# First calculate histogram
	histogram = cv2.calcHist([img],[0],None,[256],[0,255]) 
	
	# Normalize obtained histogram	
	cv2.normalize(histogram,histogram,0,255,cv2.NORM_MINMAX)
		
	return histogram


def printHistogram(histogram,canvas,withColor):

	h = np.int32(np.around(histogram))
	pts = np.column_stack((bins,h))
	color = None
	if withColor:
		color = (rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))
	else:
		color = 50

	cv2.polylines(canvas,np.array([pts],np.int32),False,color,2)

	return canvas


def main():

	print usage

	pause = False
	speed = 20

	vid = cv2.VideoCapture("videos/FamilyGuy.mp4")

	# Create list in which captured frames are stored
	frames = []

	histResult = np.zeros((300,255,3))

	# Create window
	cv2.namedWindow("Histograms")
	cv.MoveWindow("Histograms",600,20)

	while True: 

		if not pause:
			succesFlag , frameOriginal = vid.read()
			frame = cv2.cvtColor(frameOriginal,cv.CV_RGB2GRAY)

		key = cv2.waitKey(speed)

		if (key == 112):  # press 'P'
			pause = not pause
			if pause:
				print "PAUSE"
			else:
				print "RESUME"

		if (key == 115):  # press 'S'
			speed += 5
			print "speed: "+str(speed)

		if (key == 102):  # press 'F'
			if speed != 5:
				speed -= 5
				print "speed: "+str(speed)

		if (key == 114):  # press 'R'
			histResult = np.zeros((300,255,3))
			print "Histograms window cleared"


		if (key == 32):   # press SPACE
			n = len(frames)
			print "Frame %d captured"%(n)
			capture = frame.copy()
			frames.append(capture)


			hist = getHistogram(img= capture)

			histResult = printHistogram(histogram= hist, canvas= histResult, withColor= True)

			capture = printHistogram(histogram= hist, canvas= capture, withColor= False)

			cv2.imshow("frame %d capture"%(n),cv2.pyrDown(capture))
			a = None
			if (n%12 < 6):
				a = 410
			else:
				a = 550
			cv.MoveWindow("frame %d capture"%(n),(n%6)*190 + 50,a)

		hh = getHistogram(img= frame)
		frame = printHistogram(histogram= hh, canvas= frame , withColor= False)
		
		cv2.imshow("ORIGINAL",frame)
		cv.MoveWindow("ORIGINAL",50,20)

		if (len(frames) > 0):
			#for img in frames:

			cv2.imshow("Histograms",histResult)  
	
		if debugging:
			cv2.imshow("FAMILY GUY Snippet [ORIGINAL]",cv2.pyrDown(frameOriginal))
			cv.MoveWindow("FAMILY GUY Snippet [ORIGINAL]",800,415)

		if (key == 27 or key == 113):
			print "Quit"
			break



if __name__ == '__main__':
	main()

