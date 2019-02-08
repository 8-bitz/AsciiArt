from  PIL import Image, ImageDraw, ImageFont								#import from Python image library
import cv2																	#import cv2 for video editing
import os																	#import OS for file access
import subprocess															#import subprocess for accessing ffmpeg

sourceFPS = 0																#global variable for FPS
brightnessAdjustment = -5													#global variable for brightness adjustment of greyscale image

#NOTES:
# - change output size of video


def imgToAscii(imgFile):
	divisor = 3.642857142857143 #255 shades of grey per pixel.  Div by this to assign 255 shades to one ASCII character
	maxWidth = 160				#Max pixel width of resized image
	global brightnessAdjustment	#access the global variables
	asciiArt = " "				#output string
	#Greyscale to ASCII characters
	greyscaleChars = {
		"70" : "$","69" : "@","68" : "B","67" : "%","66" : "8","65" : "&","64" : "W","63" : "M","62" : "#","61" : "*","60" : "o","59" : "a","58" : "h","57" : "k","56" : "b","55" : "d","54" : "p","53" : "q","52" : "w",
		"51" : "m","50" : "Z","49" : "O","48" : "0","47" : "Q","46" : "L","45" : "C","44" : "J","43" : "U","42" : "Y","41" : "X","40" : "z","39" : "c","38" : "v","37" : "u","36" : "n","35" : "x","34" : "r","33" : "j",
		"32" : "f","31" : "t","30" : "/","29" : "\\","28" : "|","27" : "(","26" : ")","25" : "1","24" : "{","23" : "}","22" : "[","21" : "]","20" : "?","19" : "-","18" : "_","17" : "+","16" : "~","15" : "<","14" : ">",
		"13" : "i","12" : "!","11" : "l","10" : "I","9" : ";","8" : ":","7" : ",","6" : "\"","5" : "^","4" : "`","3" : "'","2" : ".","1" :  " "	,"0" :  " "
		}
	#Greyscale to ASCII characters reversed
	greyscaleCharsRev = {
		"0" : "$","1" : "@","2" : "B","3" : "%","4" : "8","5" : "&","6" : "W","7" : "M","8" : "#","9" : "*","10" : "o","11" : "a","12" : "h","13" : "k","14" : "b","15" : "d","16" : "p","17" : "q","18" : "w",
		"19" : "m","20" : "Z","21" : "O","22" : "0","23" : "Q","24" : "L","25" : "C","26" : "J","27" : "U","28" : "Y","29" : "X","30" : "z","31" : "c","32" : "v","33" : "u","34" : "n","35" : "x","36" : "r","37" : "j",
		"38" : "f","39" : "t","40" : "/","41" : "\\","42" : "|","43" : "(","44" : ")","45" : "1","46" : "{","47" : "}","48" : "[","49" : "]","50" : "?","51" : "-","52" : "_","53" : "+","54" : "~","55" : "<","56" : ">",
		"57" : "i","58" : "!","59" : "l","60" : "I","61" : ";","62" : ":","63" : ",","64" : "\"","65" : "^","66" : "`","67" : "'","68" : ".","69" :  " "	,"70" :  " "
		}
	img = Image.open(imgFile)													#Open the image file
	gImg = img.convert("L")														#Convert image to greyscaleChars
	size = gImg.size															#Get the size
	shrinkRatio = size[0] / maxWidth											#Get the ratio to shring by to make it the max Width
	gImg = gImg.resize((int(size[0]/shrinkRatio) ,int(size[1]/shrinkRatio)))	#Resize the image	
	size = gImg.size															#get new size of the image
	for y in range (0,size[1]):													#For ever row.  0,0 is the top left.
		for x in range (0,size[0]):												#For every column
			pix = gImg.getpixel((x,y))											#Get the pixel shade (0 - 255)			
			pix = brightnessAdjust(pix, brightnessAdjustment)					#adjust the brightness of the individual pixel			
			pix = int(pix / divisor)											#assign pixel shade to an ascii character
			asciiArt = 	asciiArt + greyscaleChars[str(pix)]						#Create the output string
		asciiArt = 	asciiArt + "\n "											#new line after all columns in the row are completed
	return asciiArt																#return final image

	
def videoToFrames_Grey(vidFile):											
	fileList = []																#init empty list to store file names and track order
	maxWidth = 160																#specify max width of resized frames
	global sourceFPS															#access global variable storing video FPS
	vidcap = cv2.VideoCapture(vidFile)											#access the source video file
	sourceFPS = vidcap.get(cv2.CAP_PROP_FPS)									#determine the FPS of the video file
	success,image = vidcap.read()												#read the first frame of the video
	count = 0																	#initialize a coutner to track frame numbers
	while success:																#while successfully reading frames
		width, height, _ = image.shape											#get the frame dimensions
		shrinkRatio = width / maxWidth											#Get the ratio to shrink by to make it the max Width
		image = cv2.resize(image, (int(height/shrinkRatio),int(width/shrinkRatio)))	#resize the frame
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)							#convert frame to greyscale
		cv2.imwrite("frame%d.jpg" % count, image)     							#save frame as JPEG file
		fileList.append("frame%d.jpg" % count)									#append filename to list
		success,image = vidcap.read()											#read the next frame
		print("Frame " + str(count) + " successfully read")						#print to console
		count += 1																#increment the counter
	return(fileList)															#return the file list

def stringToImage(imgText, width, height, imgName):
	img = Image.new("L", (width, height))												#create a blank image with the specified dimensions
	draw = ImageDraw.Draw(img)															#crete a draw object
	font = ImageFont.truetype("cour.ttf", 16)											#create a font object
	draw.multiline_text((0, 0), str(imgText), fill=(255), font=font, align="center")	#add the text to the image
	img.save(imgName)																	#save the image

def imagesToMovie(fileList, videoname):									
	global sourceFPS																							#access the global sourceFPS variable
	frameRate = sourceFPS																						#set the framerate variable
	frame = cv2.imread(fileList[0])																				#read the first frame from the file list
	height, width, layers = frame.shape																			#get the image dimensions

	video = cv2.VideoWriter(videoname, cv2.VideoWriter_fourcc('M','J','P','G'),frameRate,(width, height))		#create a new video encoded with MJPG

	for f in fileList:																							#for every image in the file list
		frame = cv2.imread(f)																					#read the frame
		video.write(frame)																						#write the frame to the video	
	video.release()																								#save the video
	

def brightnessAdjust(value, percent):
	max = 255												#max pixel brightness
	newValue = 0											#init new pixel value
	percent = percent / 100									#convert percentage to decimal
	newValue = int((value * percent) + value)				#add or sub percentage from original value

	if newValue > 255:										#if new value past the max threshold
		newValue = 255										#cap at 255
	elif newValue < 0:										#if below
		newValue = 0										#cap at 0
	return newValue											#return the new value

def transferAudioBetweenVideos(vidSrc, vidDst):
	audioFileName = "srcAudio.wav"																														#file name for audio export
	p = subprocess.Popen(["ffmpeg", "-i", vidSrc, "-ab", "160k", "-ac", "2", "-ar", "44100", "-vn", audioFileName], stdout=subprocess.PIPE)				#create process for extracting audio
	print (p.communicate())																																#print output

	p = subprocess.Popen(["ffmpeg", "-i", vidDst, "-i", audioFileName, "-codec", "copy", "-shortest", ("audio_" + vidDst)], stdout=subprocess.PIPE)		#overlay new audio file on video to temp video file
	print (p.communicate())																																#print output
	
	os.remove(vidDst)																																	#remove video with no audio
	os.remove(audioFileName)																															#remove temp audio file
	os.rename(("audio_" + vidDst), vidDst)																												#rename the temp video with audio


def main():	
	horiMultiplyer = 10														#pixel width for a single character
	vertMultiplyer = 18														#pixel height for a single character
	asciiFileNames = []														#list of images converted to ascii

	fileNames = videoToFrames_Grey("TEST.MOV")								#call process to convert video to frames and store file names

	for n in fileNames:														#for every file name
		art = (imgToAscii(n))												#convert image to a string of ASCII characters
		artList = art.split("\n")											#split based on lines to determine image dimensions
		imgHeight = int(len(artList) * vertMultiplyer)						#get number of rows
		imgWidth = int(len(artList[0]) * horiMultiplyer)					#get characters per line
		asciiFileNames.append("a" + n)										#add string to ascii image file name to list
		stringToImage(art, imgWidth,imgHeight, ("a" + n))					#convert string to ascii image
		print("Converted:\t" + n)											#print to console
		os.remove(n)														#cleanup the original greyscale image

	imagesToMovie(asciiFileNames, "asciiVideo.avi")							#convert images to movie
	transferAudioBetweenVideos("TEST.MOV","asciiVideo.avi")					#transfer audio from source movie to ascii movie

	for n in asciiFileNames:												#cleanup ascii images
		os.remove(n)														#remove the file 


if __name__ == "__main__":
	main()
