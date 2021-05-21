import picounicorn
from common import hsv_to_rgb

#Function to clear display by setting pixels to black
def cleardisplay():
    for x in range(picounicorn.get_width()):
        for y in range(picounicorn.get_height()):
            picounicorn.set_pixel(x, y, 0, 0, 0)            

#Function to update display with letters/numbers
def updatedisplay(displaymap, colourdict):
    x=0
    y=0
    for row in displaymap: 
        for line in row:
            for char in line:
                if x < picounicorn.get_width() and y < picounicorn.get_height():
                    if char in colourdict.keys():
                        if colourdict.get(char) == "random":
                            r, g, b = [int(c * 255) for c in hsv_to_rgb(x / picounicorn.get_width(), y / picounicorn.get_height(), 1.0)]
                        else:
                            r, g, b = colourdict[char]
                    else:
                        r, g, b = colourdict["unassigned"]
                    picounicorn.set_pixel(x, y, r, g, b)    
                x+=1
            x=0
        y+=1
    return displaymap

#Function to make the "display map" seem as though it is "scrolling" (loop)
def scrolldisplay(displaymap):
    scrollmap=[]
    rowcount=0
    for row in displaymap:
        scrollmap.append([])
        for line in row:
            scrollmap[rowcount]= [line[1:]+line[0]]
        rowcount+=1
    return scrollmap
