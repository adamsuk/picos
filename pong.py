#Import libraries
import picounicorn
import utime
from common import hsv_to_rgb
from alphanumerics import scoredict, textdict
from picodisplay import cleardisplay, updatedisplay, scrolldisplay


class PicoGames:
    def __init__(self):
        self.pu = picounicorn.init()

        #Define setup variables
        w = self.pu.get_width()#16
        h = self.pu.get_height()#7
        startballx=7
        startbally=3
        startdirH=1
        startdirV=0
        startscoreXY=0
        startscoreAB=0
        onlistAB=[2,3,4]
        onlistXY=[2,3,4]

        #Create lists of pixels for the height/width of the whole display/ball area
        listW=[]#makes a list 0-15
        for i in range(w):
            listW.append(i)

        listH=[]#makes a list 0-6
        for i in range(h):
            listH.append(i)
            
        listWball=[]#makes a list 1-14
        for i in range(1,15):
            listWball.append(i)

        listHball=[]#makes a list 0-6
        for i in range(0,7):
            listHball.append(i)
            

        # Define colours
        playerXYcolours=(0,114,178)
        playerABcolours=(255,70,160)
        ballcolours=playerABcolours
        
        self.colourmap = {"X": [255,255,255],
                          "R": [int(c * 255) for c in hsv_to_rgb(x / w, y / h, 1.0)],
                          "D": [200,200,40],
                          "A": playerABcolours,
                          "Y": playerXYcolours,
                          "unassigned": [0,0,0]
                          }

        #Set constant variables for pong title, scoring and win message

        pongtitle=[["RRRRRRRRRRRRRRRR"],
                   ["   R   R   R   R"],
                   [" R R R R R R R R"],
                   ["   R R R R R   R"],
                   [" RRR R R R RRR R"],
                   [" RRR   R R R   R"],
                   ["RRRRRRRRRRRRRRRR"]]

        BLANKSECTION= ["   " for i in range(h)] 


#Function to generate an 2D array to represent the current score in the format: PlayerABscore - PlayerXYscore
def generatescore(scoreAB,scoreXY):
    scoreABpix = [item.replace("X","A") for item in scoredict[scoreAB]]
    scoreXYpix = [item.replace("X","Y") for item in scoredict[scoreXY]]
    dashpix = [item.replace("X","D") for item in scoredict["dash"]]
    fulldisplay = [["{}{}{}{}{}".format(BLANKSECTION[i],scoreABpix[i],dashpix[i],scoreXYpix[i],BLANKSECTION[i])] for i in range(h)]
    return fulldisplay
    
#Function to generate a 2D array of specified text e.g. "WIN!"
def generatemessage(winningcolour):
    text1=[item.replace("X",winningcolour) for item in textdict["W"]]
    text2=[item.replace("X",winningcolour) for item in textdict["I"]]
    text3=[item.replace("X",winningcolour) for item in textdict["N"]]
    text4=[item.replace("X",winningcolour) for item in textdict["!"]]
    fulldisplay = [["{} {} {} {}   ".format(text1[i],text2[i],text3[i],text4[i])] for i in range(h)]
    return fulldisplay


#Display the title screen for 2 seconds
updatedisplay(pongtitle)
utime.sleep(2)

#Function to create the ball and ball trail(using previous ball co-ords)
def ball(currentballx,currentbally,prevballx,prevbally,prevball2x,prevball2y,ballcolours):
    for x in listWball:
        for y in listHball:
            if x == currentballx:
                if y == currentbally:
                    r,g,b=ballcolours
                    self.pu.set_pixel(x, y, r, g, b)
            elif x == prevballx:
                if y == prevbally:
                    r,g,b=[round(element * 0.3) for element in ballcolours]
                    self.pu.set_pixel(x, y, r, g, b)
            elif x == prevball2x:
                if y == prevball2y:
                    r,g,b=[round(element * 0.2) for element in ballcolours]
                    self.pu.set_pixel(x, y, r, g, b)          
            else:
                r,g,b=0,0,0
                self.pu.set_pixel(x, y, r, g, b)
    return currentballx,currentbally,prevballx,prevbally,prevball2x,prevball2y

#Initial invocation of "ball" function
ball(startballx,startbally,startballx,startbally,startballx,startbally,ballcolours)

ballx=startballx
bally=startbally
dirH=startdirH
dirV=startdirV
scoreAB=startscoreAB
scoreXY=startscoreXY

#Function to create playerAB paddle (in the first column)
def lightcontrolAB(onlistAB):
    for x in range(1):
        for y in listH:
            if y in onlistAB:
                r,g,b=playerABcolours
            else:
                r,g,b=0,0,0
            self.pu.set_pixel(x, y, r, g, b)
                
#Function to create playerXY paddle (in the last column)
def lightcontrolXY(onlistXY):
    for x in range(15,16):
        for y in listH:
            if y in onlistXY:
                r,g,b=playerXYcolours
            else:
                r,g,b=0,0,0
            self.pu.set_pixel(x, y, r, g, b)
  
#Function to determine the ball colour & direction (based on it's position)and update scoring
def ballposition(currentballx,currentbally,currentdirH,currentdirV,scoreAB,scoreXY,ballcolours,startdirH):
    if currentballx == listWball[0]:#if ball is in the furthest left column
        ballcolours=playerABcolours
        if currentbally in onlistAB:
            currentdirH=1
            if currentbally == onlistAB[0]:
                currentdirV=-1
            if currentbally == onlistAB[2]:
                currentdirV=1
        else:
            scoreXY+=1
            startdirH=1
            currentballx=startballx
            currentbally=startbally
            currentdirH=startdirH
            currentdirV=startdirV
            cleardisplay()
            updatedisplay(generatescore(scoreAB,scoreXY))
            utime.sleep(1)
    elif currentballx == listWball[-1]:#if ball is in the furthest right column
        ballcolours=playerXYcolours
        if currentbally in onlistXY:
            currentdirH= -1
            if currentbally == onlistXY[0]:
                currentdirV=-1
            if currentbally == onlistXY[2]:
                currentdirV=1 
        else:
            scoreAB+=1
            startdirH=- 1
            currentballx=startballx
            currentbally=startbally
            currentdirH=startdirH
            currentdirV=startdirV
            cleardisplay()
            updatedisplay(generatescore(scoreAB,scoreXY))
            utime.sleep(1)
    elif currentballx in listWball:
        if currentbally == listHball[0]:
            currentdirV=1
        elif currentbally == listHball[-1]:
            currentdirV=-1
    prevball2x=currentballx-currentdirH
    prevball2y=currentbally-currentdirV
    prevballx=currentballx
    prevbally=currentbally
    currentballx=currentballx+currentdirH
    currentbally=currentbally+currentdirV
    ball(currentballx,currentbally,prevballx,prevbally,prevball2x,prevball2y,ballcolours)
    return currentballx,currentbally,currentdirH,currentdirV,scoreAB,scoreXY,ballcolours,startdirH

#Function which runs the game       
while True:
    ballx,bally,dirH,dirV,scoreAB,scoreXY,ballcolours,startdirH = ballposition(ballx,bally,dirH,dirV,scoreAB,scoreXY,ballcolours,startdirH)
    if scoreAB >=5 or scoreXY >=5:
        if scoreAB>=5:
            winningcolour="A"
        else:
            winningcolour="Y"
        cleardisplay()
        currentdisplaymap=updatedisplay(generatemessage(winningcolour))
        for i in range(w*3):
            currentdisplaymap=updatedisplay(scrolldisplay(currentdisplaymap))
            utime.sleep(0.1)
        break
    else:
        if self.pu.is_pressed(self.pu.BUTTON_A):
            if onlistAB[0]!=0:
                onlistAB.insert(0,onlistAB[0]-1)
                onlistAB=onlistAB[:-1]
        elif self.pu.is_pressed(self.pu.BUTTON_B):
            if onlistAB[-1]!=6:
                onlistAB.insert(len(onlistAB),onlistAB[-1]+1)
                onlistAB=onlistAB[1:]
        if self.pu.is_pressed(self.pu.BUTTON_X):
            if onlistXY[0]!=0:
                onlistXY.insert(0,onlistXY[0]-1)
                onlistXY=onlistXY[:-1]
        elif self.pu.is_pressed(self.pu.BUTTON_Y):
            
            if onlistXY[-1]!=6:
                onlistXY.insert(len(onlistXY),onlistXY[-1]+1)
                onlistXY=onlistXY[1:]
    lightcontrolAB(onlistAB)
    lightcontrolXY(onlistXY)
    utime.sleep(0.1)

    