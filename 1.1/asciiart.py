from  PIL import Image, ImageDraw, ImageFont
import cv2
import os

#NOTES:
# - Make text and frames bigger to try and help quality - Will have to recalc char pix size

def imgToAscii(imgFile):
	divisor = 3.642857142857143 #255 shades of grey per pixel.  Div by this to assign 255 shades to one ASCII character
	maxWidth = 160				#Max pixel width of resized image
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
	img = Image.open(imgFile)			#Open the image file
	gImg = img.convert("L")				#Convert image to greyscaleChars
	size = gImg.size					#Get the size
	shrinkRatio = size[0] / maxWidth	#Get the ratio to shring by to make it the max Width
	gImg = gImg.resize((int(size[0]/shrinkRatio) ,int(size[1]/shrinkRatio)))	#Resize the image
	#gImg.save("tmp.jpg")				#Write a copy to disk for reference.  Will not overwrite existing file.
	size = gImg.size					#get new size of the image
	for y in range (0,size[1]):			#For ever row.  0,0 is the top left.
		for x in range (0,size[0]):		#For every column
			pix = gImg.getpixel((x,y))	#Get the pixel shade (0 - 255)
			#print("old pix: " + str(pix))
			pix = contrastAdjustUp(pix, 5)
			#print("\tnew pix: " + str(pix))
			#input("pause")
			pix = int(pix / divisor)	#assign pixel shade to an ascii character
			asciiArt = 	asciiArt + greyscaleChars[str(pix)]		#Create the output string
		asciiArt = 	asciiArt + "\n "	#new line after all columns in the row are completed
	return asciiArt						#return final image

def videoToFrames(vidFile):
	maxWidth = 160
	vidcap = cv2.VideoCapture(vidFile)
	success,image = vidcap.read()
	count = 0
	while success:
		width, height, _ = image.shape
		shrinkRatio = width / maxWidth	#Get the ratio to shring by to make it the max Width
		image = cv2.resize(image, (int(height/shrinkRatio),int(width/shrinkRatio)))
		cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
		success,image = vidcap.read()
		print('Read a new frame: ', success)
		count += 1

def videoToFrames_Grey(vidFile):
	fileList = []
	maxWidth = 160
	vidcap = cv2.VideoCapture(vidFile)
	success,image = vidcap.read()
	count = 0
	while success:
		width, height, _ = image.shape
		shrinkRatio = width / maxWidth	#Get the ratio to shring by to make it the max Width
		image = cv2.resize(image, (int(height/shrinkRatio),int(width/shrinkRatio)))
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
		fileList.append("frame%d.jpg" % count)
		success,image = vidcap.read()
		print("Frame " + str(count) + " successfully read")
		count += 1
	return(fileList)

def stringToImage(imgText, width, height, imgName):
	img = Image.new("L", (width, height))
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("cour.ttf", 16)
	#draw.text((0, 0), "Your Text Here", fill=(255), font=font)
	#print(imgText)
	draw.multiline_text((0, 0), str(imgText), fill=(255), font=font, align="center")
	img.save(imgName)

def imagesToMovie(fileList, videoname):
	#videoname = "AsciiFilms.avi"
	frame = cv2.imread(fileList[0])
	height, width, layers = frame.shape

	video = cv2.VideoWriter("colourVid_" + videoname, cv2.VideoWriter_fourcc('M','J','P','G'),30,(width, height))
	#video = cv2.VideoWriter("2" + videoname, 0,30,(width, height),0)
	#video = cv2.VideoWriter(filename=videoname, fps=30, frameSize=(width, height))

	for f in fileList:
		frame = cv2.imread(f)
		video.write(frame)
	#cv2.destroyAllWindows()
	video.release()

	video = cv2.VideoWriter("grayvid_" + videoname, cv2.VideoWriter_fourcc('M','J','P','G'),30,(width, height),False)
	for f in fileList:
		frame = cv2.imread(f)
		video.write(frame)
	#cv2.destroyAllWindows()
	video.release()

def contrastAdjustUp(value, percent):
	max = 255
	newValue = 0
	percent = percent / 100
	#print("percent: " + str(percent))
	#print("orig: " + str(value))
	#print("to add: " + str(int((value * percent))))
	newValue = int((value * percent) + value)
	#print("new value: " + str(newValue))

	if newValue > 255:
		newValue = 255
	return newValue


def main():
	horiMultiplyer = 6.09375
	vertMultiplyer = 12.90
	asciiFileNames = []

	fileNames = videoToFrames_Grey("TEST.MOV")

	#sort out pixel size here
	x = imgToAscii("cookie.jpg")
	print(x)
	stringToImage(x, 1620,1800, "x.jpg")   #calc new pix width
	input("pause")
	#********************************************************

	for n in fileNames:
		art = (imgToAscii(n))
		artList = art.split("\n")
		imgHeight = int(len(artList) * vertMultiplyer)
		imgWidth = int(len(artList[0]) * horiMultiplyer)
		asciiFileNames.append("a" + n)
		stringToImage(art, imgWidth,imgHeight, ("a" + n))
		print("Converted:\t" + n)
		os.remove(n)

	imagesToMovie(asciiFileNames, "asciiVideo.avi")

	for n in asciiFileNames:
		os.remove(n)


if __name__ == "__main__":
	main()
