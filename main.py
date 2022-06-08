import picounicorn
import utime
import os
import sys
import gc
import _thread

from common import textdict, cleardisplay, updatedisplay, scrolldisplay
import games

class PicoOS:
    def __init__(self):
        picounicorn.init()
        self.initialise_variables()
        
        # Define colours
        self.playercolours=(255,70,160)
        
        self.colourmap = {"X": [255,255,255],
                          "R": "random",
                          "D": [200,200,40],
                          "P": self.playercolours,
                          "unassigned": [0,0,0]
                          }

        #Set constant variables for title
        title=["XXXXXXXXXXXXXXXXX",
               "   X XXXXX   XX  ",
               " X XXXXXXX X X XX",
               "   X X   X X X   ",
               " XXX X XXX X XXX ",
               " XXX X   X   X  X",
               "XXXXXXXXXXXXXXXXX"]
        BLANKSECTION= ["XXX" for i in range(picounicorn.get_height())]
        fulldisplay = [[f"{BLANKSECTION[i]}{title[i]}{BLANKSECTION[i]}"] for i in range(picounicorn.get_height())]

        # Display the title screen and start display thread
        currentdisplaymap = updatedisplay(fulldisplay, self.colourmap)
        end = utime.ticks_add(utime.ticks_ms(), 2000)
        while utime.ticks_diff(end, utime.ticks_ms()) > 0:
            currentdisplaymap=updatedisplay(scrolldisplay(currentdisplaymap),
                                            self.colourmap)
            utime.sleep(0.05)
        cleardisplay()
        
        # start the OS!
        self.run_os()
    
    def start_display_thread(self):
        """
        A thread used to display the current display map
        """
        #self.display_lock.acquire()
        while True:
            if self.kill_display_thread:
                sys.exit()
                self.display_lock.release()
            if self.displaymap:
                if self.scroll_display:
                    self.displaymap = scrolldisplay(self.displaymap)
                self.displaymap = updatedisplay(self.displaymap, self.colourmap)
                utime.sleep(0.1)
                gc.collect()

    def initialise_variables(self):
        """
        A method used to initialise key variables for the game
        """
        # display thread
        self.displaymap = None
        self.scroll_display = True
        self.kill_display_thread = False
        self.display_lock = _thread.allocate_lock()
        
        # global menu
        self.buttons_pressed = []
        self.any_button_pressed = False
        self.menu_index = 0
        self.menu_options = []
        for game in [a for a in dir(games) if not a.startswith('__') and not a.endswith('__')]:
            self.menu_options.append({
                "name": game.upper(),
                "executable": getattr(games, game)
            })
        
        # generic display
        self.displayW = picounicorn.get_width() - 1
        self.displayH = picounicorn.get_height() - 1

    def generatemessage(self, colour, message):
        BLANKSECTION= [" " for i in range(self.displayH)]
        text_lst = []
        for char in message:
            text_lst.append([item.replace("X",colour) for item in textdict[char]])
            text_lst.append(BLANKSECTION)
        fulldisplay = [["".join(row) + ((self.displayW - len(row)) * " ")] for row in list(zip(*text_lst))]
        return fulldisplay
    
    def check_buttons(self, preserve_buttons=False):
        if not preserve_buttons:
            self.any_button_pressed = False
            self.buttons_pressed = []
        if picounicorn.is_pressed(picounicorn.BUTTON_A):
            self.buttons_pressed.append("A")
        if picounicorn.is_pressed(picounicorn.BUTTON_B):
            self.buttons_pressed.append("B")
        if picounicorn.is_pressed(picounicorn.BUTTON_X):
            self.buttons_pressed.append("X")
        if picounicorn.is_pressed(picounicorn.BUTTON_Y):
            self.buttons_pressed.append("Y")
        if self.buttons_pressed:
            self.any_button_pressed = True

    def run_os(self):
        self.display_lock.acquire()
        _thread.start_new_thread(self.start_display_thread, ())
        while True:
            utime.sleep(0.1)
            self.check_buttons()
            self.menu_option = self.menu_options[self.menu_index]
            self.displaymap = self.generatemessage("P", self.menu_option["name"])
            if picounicorn.is_pressed(picounicorn.BUTTON_A):
                print(self.menu_index)
                print(self.menu_option)
                if self.menu_index == 0:
                    self.menu_index = len(self.menu_options) - 1
                else:
                    self.menu_index -= 1
                self.menu_option = self.menu_options[self.menu_index]
                self.displaymap = self.generatemessage("P", self.menu_option["name"])
            if picounicorn.is_pressed(picounicorn.BUTTON_B):
                print(self.menu_index)
                print(self.menu_option)
                if self.menu_index == len(self.menu_options) - 1:
                    self.menu_index = 0
                else:
                    self.menu_index += 1
                self.menu_option = self.menu_options[self.menu_index]
                self.displaymap = self.generatemessage("P", self.menu_option["name"])
            if picounicorn.is_pressed(picounicorn.BUTTON_Y):
                utime.sleep(0.1)
                self.kill_display_thread = True
                utime.sleep(0.1)
                gc.collect()
                cleardisplay()
                self.initialise_variables()
                self.display_lock.acquire()
                self.menu_option["executable"]()
                utime.sleep(0.1)
                self.display_lock.release()
                gc.collect()
                cleardisplay()
                self.display_lock.acquire()
                _thread.start_new_thread(self.start_display_thread, ())

if __name__ == "__main__":
    PicoOS()
