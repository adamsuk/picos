
#Function to clear display by setting pixels to black
def cleardisplay(picounicorn):
    for x in range(w):
        for y in range(h):
            picounicorn.set_pixel(x, y, 0, 0, 0)            

#Function to update display with letters/numbers
def updatedisplay(picounicorn, displaymap, colourdict):
    x=0
    y=0
    for row in displaymap: 
        for line in row:
            for char in line:
                if x < w and y <h:
                    if char in colourdict.keys():  
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
