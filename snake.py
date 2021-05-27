#Import libraries
import picounicorn
import utime
from alphanumerics import scoredict, textdict
from display import cleardisplay, updatedisplay, scrolldisplay


class PicoGames:
    def __init__(self):
        picounicorn.init()

        #Define setup variables
        self.winning_score = 9
        self.wall_reflect = False
        self.initialise_variables()
        
        # Define colours
        self.playercolours=(255,70,160)
        self.ballcolours=self.playercolours
        
        self.colourmap = {"X": [255,255,255],
                          "R": "random",
                          "D": [200,200,40],
                          "P": self.playercolours,
                          "unassigned": [0,0,0]
                          }

        #Set constant variables for title
        title=[["RRRRRRRRRRRRRRRR"],
               ["RRRRRRRRRRRRRRRR"],
               ["RRRRRRRRRRRRRRRR"],
               ["RRRRRRRRRRRRRRRR"],
               ["RRRRRRRRRRRRRRRR"],
               ["RRRRRRRRRRRRRRRR"],
               ["RRRRRRRRRRRRRRRR"]]
            
        #Display the title screen for 2 seconds
        updatedisplay(title, self.colourmap)
        utime.sleep(2)

        #Initial invocation of "ball" function
        self.snake()
        
        # start the game!
        self.run_game()

    def initialise_variables(self):
        """
        A method used to initialise key variables for the game
        """
        self.startballx=7
        self.startbally=3
        self.startdirH=1
        self.startdirV=0
        self.ballx=self.startballx
        self.bally=self.startbally
        self.dirH=self.startdirH
        self.dirV=self.startdirV
        self.score=0

        #Create lists of pixels for the height/width of the whole display/ball area
        self.listW=[]#makes a list 0-15
        for i in range(picounicorn.get_width()):
            self.listW.append(i)

        self.listH=[]#makes a list 0-6
        for i in range(picounicorn.get_height()):
            self.listH.append(i)
    
    #Function to generate an 2D array to represent the current score in the format: PlayerABscore - PlayerXYscore
    def generatescore(self):
        scorepix = [item.replace("X","P") for item in scoredict[self.score]]
        fulldisplay = [["{}".format(scorepix[i])] for i in range(picounicorn.get_height())]
        return fulldisplay
    
    #Function to generate a 2D array of specified text e.g. "WIN!"
    def generatemessage(self, winningcolour):
        text1=[item.replace("X",winningcolour) for item in textdict["W"]]
        text2=[item.replace("X",winningcolour) for item in textdict["I"]]
        text3=[item.replace("X",winningcolour) for item in textdict["N"]]
        text4=[item.replace("X",winningcolour) for item in textdict["!"]]
        fulldisplay = [["{} {} {} {}   ".format(text1[i],text2[i],text3[i],text4[i])] for i in range(picounicorn.get_height())]
        return fulldisplay

    #Function to create the snake and trail(using previous co-ords)
    def snake(self):
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
                        picounicorn.set_pixel(x, y, r, g, b)
                elif x == prevballx:
                    if y == prevbally:
                        r,g,b=[round(element * 0.3) for element in self.ballcolours]
                        picounicorn.set_pixel(x, y, r, g, b)
                elif x == prevball2x:
                    if y == prevball2y:
                        r,g,b=[round(element * 0.2) for element in self.ballcolours]
                        picounicorn.set_pixel(x, y, r, g, b)
                else:
                    r,g,b=0,0,0
                    picounicorn.set_pixel(x, y, r, g, b)
        return self.ballx,self.bally,prevballx,prevbally,prevball2x,prevball2y

    #Function to determine the ball colour & direction (based on it's position)and update scoring
    def ballposition(self):
        if self.ballx == self.listWball[0]:#if ball is in the furthest left column
            self.ballcolours=self.playerABcolours
            if self.bally in self.onlistAB:
                self.dirH=1
                if self.bally == self.onlistAB[0] and self.dirV == 0:
                    self.dirV = -1
                elif self.bally == self.onlistAB[1]:
                    self.dirV = 0
                elif self.bally == self.onlistAB[-1] and self.dirV == 0:
                    self.dirV = 1
                elif self.bally in [self.listHball[0], self.listHball[-1]]:
                    self.dirV *= -1
            elif self.bally == self.onlistAB[0] -1 and self.dirV == 1:
                self.dirH = 1
                self.dirV = -1
            elif self.bally == self.onlistAB[-1] +1 and self.dirV == -1:
                self.dirH = 1
                self.dirV = 1
            else:
                self.scoreXY+=1
                self.startdirH=1
                self.ballx=self.startballx
                self.bally=self.startbally
                self.dirH=self.startdirH
                self.dirV=self.startdirV
                cleardisplay()
                updatedisplay(self.generatescore(), self.colourmap)
                utime.sleep(1)
        elif self.ballx == self.listWball[-1]:#if ball is in the furthest right column
            self.ballcolours=self.playerXYcolours
            if self.bally in self.onlistXY:
                self.dirH=-1
                if self.bally == self.onlistXY[0] and self.dirV == 0:
                    self.dirV = -1
                elif self.bally == self.onlistXY[1]:
                    self.dirV = 0
                elif self.bally == self.onlistXY[-1] and self.dirV == 0:
                    self.dirV = 1
                elif self.bally in [self.listHball[0], self.listHball[-1]]:
                    self.dirV *= -1
            elif self.bally == self.onlistXY[0] -1 and self.dirV == 1:
                self.dirH = 1
                self.dirV = -1
            elif self.bally == self.onlistXY[-1] +1 and self.dirV == -1:
                self.dirH = 1
                self.dirV = 1
            else:
                self.scoreAB+=1
                self.startdirH=- 1
                self.ballx=self.startballx
                self.bally=self.startbally
                self.dirH=self.startdirH
                self.dirV=self.startdirV
                cleardisplay()
                updatedisplay(self.generatescore(), self.colourmap)
                utime.sleep(1)
        # reflect off wall
        elif self.ballx in self.listWball and self.wall_reflect:
            if self.bally == self.listHball[0]:
                self.dirV=1
            elif self.bally == self.listHball[-1]:
                self.dirV=-1
        elif self.ballx in self.listWball and not self.wall_reflect:
            if self.bally == self.listHball[0]:
                self.bally = self.listHball[-1]
            elif self.bally == self.listHball[-1]:
                self.bally = self.listHball[0]
        self.ball()
    
    def run_game(self):
        #Function which runs the game
        while True:
            self.ballposition()
            if self.score >= self.winning_score:
                cleardisplay()
                currentdisplaymap=updatedisplay(self.generatemessage("P"),
                                                self.colourmap)
                anyButton = False
                while not anyButton:
                    currentdisplaymap=updatedisplay(scrolldisplay(currentdisplaymap),
                                                    self.colourmap)
                    utime.sleep(0.1)
                    if picounicorn.is_pressed(picounicorn.BUTTON_A) or \
                        picounicorn.is_pressed(picounicorn.BUTTON_B) or \
                            picounicorn.is_pressed(picounicorn.BUTTON_X) or \
                                picounicorn.is_pressed(picounicorn.BUTTON_Y):
                        anyButton = True
                # reinitialise game
                self.initialise_variables()
                self.snake()
                self.run_game()
            else:
                if picounicorn.is_pressed(picounicorn.BUTTON_A):
                    if self.onlistAB[0]!=0:
                        self.onlistAB.insert(0,self.onlistAB[0]-1)
                        self.onlistAB=self.onlistAB[:-1]
                    elif self.onlistAB[0] == 0 and self.inf_paddles:
                        self.onlistAB.insert(0,6)
                        self.onlistAB=self.onlistAB[:-1]                        
                elif picounicorn.is_pressed(picounicorn.BUTTON_B):
                    if self.onlistAB[-1]!=6:
                        self.onlistAB.insert(len(self.onlistAB),self.onlistAB[-1]+1)
                        self.onlistAB=self.onlistAB[1:]
                    elif self.onlistAB[-1] == 6 and self.inf_paddles:
                        self.onlistAB.insert(len(self.onlistAB),0)
                        self.onlistAB=self.onlistAB[1:]
                if picounicorn.is_pressed(picounicorn.BUTTON_X):
                    if self.onlistXY[0]!=0:
                        self.onlistXY.insert(0,self.onlistXY[0]-1)
                        self.onlistXY=self.onlistXY[:-1]
                    elif self.onlistXY[0] == 0 and self.inf_paddles:
                        self.onlistXY.insert(0,6)
                        self.onlistXY=self.onlistXY[:-1]
                elif picounicorn.is_pressed(picounicorn.BUTTON_Y):
                    if self.onlistXY[-1]!=6:
                        self.onlistXY.insert(len(self.onlistXY),self.onlistXY[-1]+1)
                        self.onlistXY=self.onlistXY[1:]
                    elif self.onlistXY[-1] == 6 and self.inf_paddles:
                        self.onlistXY.insert(len(self.onlistXY),0)
                        self.onlistXY=self.onlistXY[1:]
            utime.sleep(0.1)

if __name__ == "__main__":
    PicoGames()
