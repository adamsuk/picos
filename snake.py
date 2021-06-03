#Import libraries
import picounicorn
import utime
from alphanumerics import scoredict, textdict
from display import cleardisplay, updatedisplay, scrolldisplay


class PicoGames:
    def __init__(self):
        picounicorn.init()

        #Define setup variables
        self.score = 0
        self.alive = True
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
        title=[["                "],
               ["      RRR    R  "],
               ["     R   R  R   "],
               ["    R     RRRR  "],
               [" RRR        R   "],
               ["             R  "],
               ["                "]]
            
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
        self.snakex=[self.startballx,]
        self.snakey=[self.startbally,]
        self.dirH=self.startdirH
        self.dirV=self.startdirV

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

    # Function used to determine the current snake position
    def snake_position(self):
        # add to the snake list
        self.snakex.append(self.snakex[-1] + self.dirH)
        self.snakex = self.snakex[1:]
        self.snakey.append(self.snakey[-1] + self.dirV)
        self.snakey = self.snakey[1:]
        print(self.snakex)
        print(self.snakey)

    #Function to create the snake and trail(using previous co-ords)
    def snake(self):
        cleardisplay()
        # determine snake position
        self.snake_position()
        # iterate over the snake list and display
        for x in self.snakex:
            for y in self.snakey:
                r,g,b=self.ballcolours
                picounicorn.set_pixel(x, y, r, g, b)
    
    def run_game(self):
        #Function which runs the game
        while True:
            if not self.alive:
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
                    print("Up")
                    self.dirV = -1
                    self.dirH = 0
                elif picounicorn.is_pressed(picounicorn.BUTTON_B):
                    print("Down")
                    self.dirV = 1
                    self.dirH = 0
                if picounicorn.is_pressed(picounicorn.BUTTON_X):
                    print("Left")
                    self.dirV = 0
                    self.dirH = 1
                elif picounicorn.is_pressed(picounicorn.BUTTON_Y):
                    print("Right")
                    self.dirV = 0
                    self.dirH = -1
            utime.sleep(0.1)
            self.snake()

if __name__ == "__main__":
    PicoGames()
