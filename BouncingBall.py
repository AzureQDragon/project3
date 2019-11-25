'''
Daniel Moon
11/25/19
Project 3: Game where user needs to click moving object. Each successful click increases speed
and decreases size of object. Background changes color with wall collisions

Input: Mouse left click
Output: Messageboxes, Changing size and speed of object
'''

from tkinter import *
from tkinter import messagebox
from random import randint
from PIL import Image, ImageTk

#Handles animations of objects
def animate():
    global x1, y1, x2, y2, deltax, deltay, roundnum, colorlist

    #Constant movement update
    x1 += deltax
    x2 += deltax
    y1 += deltay
    y2 += deltay

    #Handles wall collisions and background color change
    #Dynamically changes depending on size of object
    if (x1 + (150/roundnum)) >= Canvaswidth or x1-(50/(roundnum+.5))<= 0:
        deltax = -deltax
        randcolor = randint(0,3)
        canvas.itemconfig('back', fill = colorlist[randcolor])
    if (y1 + (100/roundnum)) >= Canvasheight or y1-(5/roundnum)<= 0:
        deltay = -deltay
        randcolor = randint(0,3)
        canvas.itemconfig('back', fill = colorlist[randcolor])
    
    #Movement of object through recursion
    canvas.move('target',deltax, deltay)
    window.after(10, animate) 
    return

#Handles the changes that come from when a new round is initiated
def nextround(event):
    global x1, y1, x2, y2, deltax, deltay, target1, target2, target3, roundnum, clicks, imagedvd, finalimage
    clicks =0
    roundnum += 1

    #Prompts user if they wish to continue if round number is 3 or lower
    if roundnum <4:
        #Prompts user for whether to move on
        MsgBox = messagebox.askquestion ('You win this round!','Do you wish to move on?')

        #In the case the user says no, then the window closes
        if MsgBox == 'no':
            window.destroy()

    #Reset canvas items
    canvas.delete(target1)
    canvas.delete(target2)
    canvas.delete(target3)

    #Handles changes to velocity according to current direction
    if deltax > 0 and deltay > 0:
        deltax +=2
        deltay +=2
    elif deltax <0 and deltay > 0:
        deltax-=2
        deltay +=2
    elif deltax <0 and deltay <0:
        deltax-=2
        deltay-=2
    elif deltax>0 and deltay <0:
        deltax+=2
        deltay-=2
    
    #Changes size of object according to round tracked 
    if roundnum ==2:
        imagedvd = imagedvd.resize((60, 60), Image.ANTIALIAS)
        finalimage = ImageTk.PhotoImage(imagedvd)
    elif roundnum == 3:
        imagedvd = imagedvd.resize((50, 50), Image.ANTIALIAS)
        finalimage = ImageTk.PhotoImage(imagedvd)
    elif roundnum >= 4:
        winMessage = messagebox.showinfo('You win!', 'You won the game!')
        window.destroy()

    #New spawning coordinates generated
    y1 = randint(10, 440)
    x1 = randint(10, 440)
    x2 = (x1+70) - roundnum*20
    y2 = (y1+70) - roundnum*10
    
    #Recreate objects to render
    target3 = canvas.create_oval(x1, y1, x2+50, y2 ,outline ='', fill ='#03e8fc', tags='target') 
    target2 = canvas.create_oval(x1+10, y1+10, x2+40, y2-10, outline='', fill ='#03fc84', tags='target')   
    target1 = canvas.create_image(x1+5, y1, image = finalimage, tags='target', anchor=NW)
    return

#Tracks number of clicks not on object
def registerclick(event):
    global clicks
    clicks += 1

    #If user misses 5 times, then the program gives 'You Lose' message
    if clicks >= 5:
        MsgBox = messagebox.showinfo('You Lose', 'You have lost.')
        window.destroy()
    return

#Creation of canvas and window with size of 600x500
window = Tk()
Canvaswidth = 600
Canvasheight = 500
window.geometry(str(Canvaswidth) + 'x' + str(Canvasheight))
window.title('Catch Me if You Can!')
canvas = Canvas(window, height = Canvasheight, width = Canvaswidth)
canvas.pack()

#Global Variables
colorlist = ['#036ffc', '#fc2c03', '#03fc5e', '#ba03fc'] #Stores colors for alternating background
roundnum = 1 #Round number starts at 1 in order to allow for dynamic shape changes
clicks = 0
deltax = 2
deltay = -1

#Random starting coordinates
y1 = randint(70, 430)
x1 = randint(60, 430)

#Creating sizing coordinates for ovals
x2 = (x1+150)
y2 = (y1+100)

#Takes the image 'dvd.png' and changes the size
imagedvd = Image.open('dvd.png') #Uses PIL to open the image
imagedvd = imagedvd.resize((100, 100), Image.ANTIALIAS) #Resizes the PIL format image
finalimage = ImageTk.PhotoImage(imagedvd) #Converts to a Tkinter usable image

#Creates background
background = canvas.create_rectangle(0,0,Canvaswidth,Canvasheight, fill = 'white', tags = 'back')          
canvas.tag_bind('back', '<Button-1>', registerclick)  #Registers calls registerclick to track number of clicks

#Creates 3 items within the 'target' tag
target1 = canvas.create_oval(x1-50, y1, x2, y2, outline='', fill = '#03e8fc', tags= 'target')  
target2 = canvas.create_oval(x1-40, y1+10, x2-20, y2-20, outline='', fill = '#03fc84', tags= 'target')   
target3 = canvas.create_image(x1, y1, image = finalimage, tags='target', anchor = NW)

#Binds target to the left mouse button to register clicks
canvas.tag_bind('target', '<Button-1>', nextround)

#mainloop and first call of animate function
animate()
window.mainloop()