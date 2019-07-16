#imports pre-made functions and lists from libraries 
from wordcloud import WordCloud, STOPWORDS
#we can also rename libraries
import matplotlib.pyplot as plt
#we can import single functions
from random import randint
import tkMessageBox
#or we can import **everything**
from Tkinter import *

#global variables are available across functions, 
#even inside the function we make
global k
#k Sets word size variation, higher means more
#variation, 1 is no variation, k >=1. 
k=1


#Old command line file input--
#keeping old code commented out allows us
#to hold onto and reuse code.
#filename = str(raw_input("What is the filename for your wordcloud data (i.e. data.txt)\n"))

#Function created to be bound to both
# command button and return key
def getCloud(event):
	#path is hard-coded for ease of use
	filename = e.get()
	file_path = "/home/fergieis/Desktop/evelyn/" + filename
	file = open(file_path, "r")
	text=""

	#each line gets randomly multiplied several times 
	#allows for variation word size
	for line in file:
		for x in range(0,randint(1,k)):
			text = text+" " + line
	file.close() 

	#stopwords can be added to the stopwords set via update
	#to remove from the word cloud
	#stopwords =set(STOPWORDS)
	#stopwords.update(["word","nor","neither","nyet"])
	stopwords = set(STOPWORDS)
	stopwords.update(["and","or", "of", "the"])
	#generate the cloud and plot
	wordcloud = WordCloud(stopwords=stopwords, background_color="pink").generate(text)
	
	plt.imshow(wordcloud,interpolation='bilinear')
	plt.axis("off")

	#remove the ".txt" file extension from the filename
	#and save the image file
	filename = filename[:-4]
	plt.savefig("/home/fergieis/Desktop/evelyn/"+filename+".png")
	#plt.show()
	tkMessageBox.showinfo(title="Evelyn's Word Cloud Generator", message="Word Cloud image file saved to:\n/home/fergieis/Desktop/evelyn/"+filename+".png")
	raise SystemExit


#initialize main window
top = Tk()
top.title("Evelyn's Word Cloud Generator")

#bind return key to getCloud function
top.bind('<Return>', getCloud)

#label
l=Label(top, text="What is the filename\nfor your wordcloud data\n (i.e. data.txt)")
l.pack(side=LEFT)

#input or 'entry'
e=Entry(top, bd=5)
e.focus()
e.pack(side=RIGHT)

#button
b=Button(top, text="Press Me!",command=getCloud)
b.pack(side=BOTTOM)

#run
top.mainloop()

