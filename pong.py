#Import libraries
import picounicorn
import utime
from alphanumerics import scoredict, textdict
from picodisplay import cleardisplay, updatedisplay, scrolldisplay


class PicoGames:
    def __init__(self):
        self.pu = picounicorn.init()

        #Define setup variables
        self.startballx=7
        self.startbally=3
        self.startdirH=1
        self.startdirV=0
        self.onlistAB=[2,3,4]
        self.onlistXY=[2,3,4]
        self.ballx=self.startballx
        self.bally=self.startbally
        self.dirH=self.startdirH
        self.dirV=self.startdirV
        self.scoreAB=0
        self.scoreXY=0

        #Create lists of pixels for the height/width of the whole display/ball area
        self.listWball=[]#makes a list 1-14
        for i in range(1, self.pu.get_width()-1):
            self.listWball.append(i)

        self.listHball=[]#makes a list 0-6
        for i in range(0, self.pu.get_height()):
            self.listHball.append(i)
        
        # Define colours
        self.playerXYcolours=(0,114,178)
        self.playerABcolours=(255,70,160)
        self.ballcolours=self.playerABcolours
        
        self.colourmap = {"X": [255,255,255],
                          "R": "random",
                          "D": [200,200,40],
                          "A": self.playerABcolours,
                          "Y": self.playerXYcolours,
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
            
        #Display the title screen for 2 seconds
        updatedisplay(pongtitle)
        utime.sleep(2)

        #Initial invocation of "ball" function
        self.ball()


    #Function to generate an 2D array to represent the current score in the format: PlayerABscore - PlayerXYscore
    def generatescore(self):
        scoreABpix = [item.replace("X","A") for item in scoredict[self.scoreAB]]
        scoreXYpix = [item.replace("X","Y") for item in scoredict[self.scoreXY]]
        dashpix = [item.replace("X","D") for item in scoredict["dash"]]
        BLANKSECTION= ["   " for i in range(self.pu.get_height())]
        fulldisplay = [["{}{}{}{}{}".format(BLANKSECTION[i],scoreABpix[i],dashpix[i],scoreXYpix[i],BLANKSECTION[i])] for i in range(self.pu.get_height())]
        return fulldisplay
    
    #Function to generate a 2D array of specified text e.g. "WIN!"
    def generatemessage(self, winningcolour):
        text1=[item.replace("X",winningcolour) for item in textdict["W"]]
        text2=[item.replace("X",winningcolour) for item in textdict["I"]]
        text3=[item.replace("X",winningcolour) for item in textdict["N"]]
        text4=[item.replace("X",winningcolour) for item in textdict["!"]]
        fulldisplay = [["{} {} {} {}   ".format(text1[i],text2[i],text3[i],text4[i])] for i in range(self.pu.get_height())]
        return fulldisplay

    #Function to create the ball and ball trail(using previous ball co-ords)
    def ball(self):
        # reassign ball position
        prevball2x=self.ballx-self.dirH
        prevball2y=self.bally-self.dirV
        prevballx=self.ballx
        prevbally=self.bally
        self.ballx=self.ballx+self.dirH
        self.bally=self.bally+self.dirV
        # determine colours
        for x in self.listWball:
            for y in self.listHball:
                if x == self.ballx:
                    if y == self.bally:
                        r,g,b=self.ballcolours
                        self.pu.set_pixel(x, y, r, g, b)
                elif x == prevballx:
                    if y == prevbally:
                        r,g,b=[round(element * 0.3) for element in self.ballcolours]
                        self.pu.set_pixel(x, y, r, g, b)
                elif x == prevball2x:
                    if y == prevball2y:
                        r,g,b=[round(element * 0.2) for element in self.ballcolours]
                        self.pu.set_pixel(x, y, r, g, b)          
                else:
                    r,g,b=0,0,0
                    self.pu.set_pixel(x, y, r, g, b)
        return self.ballx,self.bally,prevballx,prevbally,prevball2x,prevball2y

    #Function to create playerAB paddle (in the first column)
    def lightcontrolAB(self):
        for x in range(1):
            for y in self.listH:
                if y in self.onlistAB:
                    r,g,b = self.playerABcolours
                else:
                    r,g,b=0,0,0
                self.pu.set_pixel(x, y, r, g, b)
    
    #Function to create playerXY paddle (in the last column)
    def lightcontrolXY(self):
        for x in range(15,16):
            for y in self.listH:
                if y in self.onlistXY:
                    r,g,b=self.playerXYcolours
                else:
                    r,g,b=0,0,0
                self.pu.set_pixel(x, y, r, g, b)
    
    #Function to determine the ball colour & direction (based on it's position)and update scoring
    def ballposition(self):
        if self.ballx == self.listWball[0]:#if ball is in the furthest left column
            self.ballcolours=self.playerABcolours
            if self.bally in self.onlistAB:
                self.dirH=1
                if self.bally == self.onlistAB[0]:
                    self.dirV=-1
                if self.bally == self.onlistAB[2]:
                    self.dirV=1
            else:
                self.scoreXY+=1
                self.startdirH=1
                self.ballx=self.startballx
                self.bally=self.startbally
                self.dirH=self.startdirH
                self.dirV=self.startdirV
                cleardisplay()
                updatedisplay(self.generatescore(self.scoreAB,self.scoreXY))
                utime.sleep(1)
        elif self.ballx == self.listWball[-1]:#if ball is in the furthest right column
            self.ballcolours=self.playerXYcolours
            if self.bally in self.onlistXY:
                self.dirH= -1
                if self.bally == self.onlistXY[0]:
                    self.dirV=-1
                if self.bally == self.onlistXY[2]:
                    self.dirV=1 
            else:
                self.scoreAB+=1
                self.startdirH=- 1
                self.ballx=self.startballx
                self.bally=self.startbally
                self.dirH=self.startdirH
                self.dirV=self.startdirV
                cleardisplay()
                updatedisplay(self.generatescore(self.scoreAB,self.scoreXY))
                utime.sleep(1)
        elif self.ballx in self.listWball:
            if self.bally == self.listHball[0]:
                self.dirV=1
            elif self.bally == self.listHball[-1]:
                self.dirV=-1
        self.ball()

    def run_game(self):
        #Function which runs the game       
        while True:
            self.ballposition()
            if self.scoreAB >=5 or self.scoreXY >=5:
                if self.scoreAB>=5:
                    winningcolour="A"
                else:
                    winningcolour="Y"
                cleardisplay()
                currentdisplaymap=updatedisplay(self.generatemessage(winningcolour))
                anyButton = False
                while not anyButton:
                    currentdisplaymap=updatedisplay(scrolldisplay(currentdisplaymap))
                    utime.sleep(0.1)
                    """
                    if self.pu.is_pressed(self.pu.BUTTON_A) or \
                        self.pu.is_pressed(self.pu.BUTTON_B) or \
                            self.pu.is_pressed(self.pu.BUTTON_X) or \
                                self.pu.is_pressed(self.pu.BUTTON_Y):
                        anyButton = True
                        break
                    """
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
            self.lightcontrolAB(onlistAB)
            self.lightcontrolXY(onlistXY)
            utime.sleep(0.1)
