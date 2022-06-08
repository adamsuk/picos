import picounicorn
import utime

# this sucks - need to look into better imports
import sys
sys.path.append("..")

from common import scoredict, textdict, cleardisplay, updatedisplay, scrolldisplay, random_int

class PicoGames:
    def __init__(self):
        picounicorn.init()

        #Define setup variables
        self.score = 0
        self.alive = True
        self.wall_loop = True
        self.cannibal = False
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
        title=[["RRR          RRR"],
               ["R    R   R R R R"],
               ["RRR      R R RRR"],
               ["  RRRR   RR  R  "],
               ["RRRR RRRRR RRRRR"],
               ["   R RR R       "],
               ["      RRRR      "]]
            
        #Display the title screen for 2 seconds
        updatedisplay(title, self.colourmap)
        utime.sleep(2)

        # Initiate game piece methods
        self.food_position()
        self.snake()
        
        # start the game!
        self.run_game()

    def initialise_variables(self):
        """
        A method used to initialise key variables for the game
        """
        self.exit_game = False
        self.eaten = True
        self.alive = True
        self.valid_button = False
        self.startballx=7
        self.startbally=3
        self.startdirH=1
        self.startdirV=0
        self.snakex=[self.startballx,]
        self.snakey=[self.startbally,]
        self.displayW = picounicorn.get_width() - 1
        self.displayH = picounicorn.get_height() - 1
        self.string_to_direction("right", set_self=True)

    #Function to generate a 2D array of specified text e.g. the final score
    def generatemessage(self, winningcolour, message):
        BLANKSECTION= [" " for i in range(self.displayH)]
        text_lst = []
        for char in message:
            text_lst.append([item.replace("X",winningcolour) for item in scoredict[int(char)]])
            text_lst.append(BLANKSECTION)
        fulldisplay = [["".join(row) + ((self.displayW - len(row)) * " ")] for row in list(zip(*text_lst))]
        return fulldisplay

    # Function used to determine the current snake position
    def snake_position(self):
        # determine new x and y positions
        new_x = self.snakex[-1] + self.dirH
        new_y = self.snakey[-1] + self.dirV
        # check for how to treat the wall
        # X
        if new_x < 0 or new_x > self.displayW:
            if self.wall_loop:
                if new_x < 0:
                    new_x = self.displayW
                else:
                    new_x = 0
                self.snakex.append(new_x)
            else:
                self.alive = False
        else:
            # add to the snake list
            self.snakex.append(new_x)
        # Y
        if new_y < 0 or new_y > self.displayH:
            if self.wall_loop:
                if new_y < 0:
                    new_y = self.displayH
                else:
                    new_y = 0
                self.snakey.append(new_y)
            else:
                self.alive = False
        else:
            self.snakey.append(new_y)
        # if fruit is not eaten move snake
        self.snake_eating()
        if not self.eaten:
            self.snakex = self.snakex[1:]
            self.snakey = self.snakey[1:]
        
        # generate the score (x and y are identical in size)
        self.score = len(self.snakex)

        # check to see if you can eat yourself
        if not self.cannibal:
            if (self.snakex[-1], self.snakey[-1]) in list(zip(self.snakex[:-1], self.snakey[:-1])):
                self.alive = False

    def snake_eating(self):
        """
        A method used to determine if a snake is eating
        """
        if (self.snakex[-1] == self.foodx) and (self.snakey[-1] == self.foody):
            self.eaten = True
        else:
            self.eaten = False

    def food_position(self):
        """
        A method for randomly generating the food location
        """
        if self.eaten:
            legal_position = False
            while not legal_position:
                self.foodx = random_int(self.displayW)
                self.foody = random_int(self.displayH)
                # check again the snake lists
                if (self.foodx not in self.snakex) or (self.foody not in self.snakey):
                    legal_position = True
        picounicorn.set_pixel(self.foodx, self.foody, *self.colourmap["D"])

    #Function to create the snake and trail(using previous co-ords)
    def snake(self):
        # determine snake position
        self.snake_position()
        # iterate over the snake list and display
        for x, y in zip(self.snakex, self.snakey):
            r,g,b=self.ballcolours
            picounicorn.set_pixel(x, y, r, g, b)
    
    def direction_to_string(self, dirV=None, dirH=None, set_self=False):
        """Converts vert and horz directions into a human readable string"""
        if not dirV:
            dirV = self.dirV
        if not dirH:
            dirH = self.dirH
        if dirV == -1 and dirH == 0:
            direction = "up"
            opposite_direction = "down"
        elif dirV == 1 and dirH == 0:
            direction = "down"
            opposite_direction = "up"
        elif dirV == 0 and dirH == -1:
            direction = "left"
            opposite_direction = "right"
        elif dirV == 0 and dirH == 1:
            direction = "right"
            opposite_direction = "left"
        if set_self:
            self.direction = direction
            self.opposite_direction = opposite_direction
        else:
            return({"direction":direction,
                    "opposite_direction":opposite_direction})
    
    def string_to_direction(self, direction=None, set_self=False):
        """Converts a human readable string into vert and horz directions"""
        if not direction:
            direction = self.direction
        if direction == "up":
            dirV = -1
            dirH = 0
        elif direction == "down":
            dirV = 1
            dirH = 0
        elif direction == "left":
            dirV = 0
            dirH = -1
        elif direction == "right":
            dirV = 0
            dirH = 1
        if set_self:
            self.dirV = dirV
            self.dirH = dirH
        else:
            return({"dirV":dirV,
                    "dirH":dirH})
    
    def run_game(self):
        #Function which runs the game
        while not self.exit_game:
            if not self.alive:
                cleardisplay()
                currentdisplaymap=updatedisplay(self.generatemessage("P", str(self.score)),
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
                        self.exit_game = True
                        anyButton = True
                
                if self.exit_game:
                    break
                # reinitialise game
                self.initialise_variables()
                self.food_position()
                self.snake()
                self.run_game()
            else:
                self.valid_button = False
                if picounicorn.is_pressed(picounicorn.BUTTON_A) and not self.valid_button:
                    if not self.direction_to_string()["opposite_direction"] == "up":
                        self.string_to_direction(direction="up", set_self=True)
                        self.valid_button = True
                elif picounicorn.is_pressed(picounicorn.BUTTON_B) and not self.valid_button:
                    if not self.direction_to_string()["opposite_direction"] == "down":
                        self.string_to_direction(direction="down", set_self=True)
                        self.valid_button = True
                if picounicorn.is_pressed(picounicorn.BUTTON_X) and not self.valid_button:
                    if not self.direction_to_string()["opposite_direction"] == "left":
                        self.string_to_direction(direction="left", set_self=True)
                        self.valid_button = True
                elif picounicorn.is_pressed(picounicorn.BUTTON_Y) and not self.valid_button:
                    if not self.direction_to_string()["opposite_direction"] == "right":
                        self.string_to_direction(direction="right", set_self=True)
                        self.valid_button = True
                if picounicorn.is_pressed(picounicorn.BUTTON_A) and \
                        picounicorn.is_pressed(picounicorn.BUTTON_X):
                    self.exit_game = True
                if self.exit_game:
                    break
            utime.sleep(0.1)
            cleardisplay()
            self.food_position()
            self.snake()

def main():
    PicoGames()

if __name__ == "__main__":
    PicoGames()
