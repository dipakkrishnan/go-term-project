# Parts taken from 112 grid demo 
########################################

                                     
#         GGGGGGGGGGGGG                 
#      GGG::::::::::::G                 
#    GG:::::::::::::::G                 
#   G:::::GGGGGGGG::::G                 
#  G:::::G       GGGGGG   ooooooooooo   
# G:::::G               oo:::::::::::oo 
# G:::::G              o:::::::::::::::o
# G:::::G    GGGGGGGGGGo:::::ooooo:::::o
# G:::::G    G::::::::Go::::o     o::::o
# G:::::G    GGGGG::::Go::::o     o::::o
# G:::::G        G::::Go::::o     o::::o
#  G:::::G       G::::Go::::o     o::::o
#   G:::::GGGGGGGG::::Go:::::ooooo:::::o
#    GG:::::::::::::::Go:::::::::::::::o
#      GGG::::::GGG:::G oo:::::::::::oo 
#         GGGGGG   GGGG   ooooooooooo   

# Author: Dipak Krishnan
# https://giphy.com/gifs/producthunt-uber-logo-3o7TKJzb15zUs5craU-uber gif 
# uber background 
# https://cdn.dribbble.com/users/249952/screenshots/1139015/cars.png car image
# uber icon
# stackoverflow.com/questions/16726354/saving-the-highscore-for-a-python-game 
# used stackoverflow to figure out matplot lib graphing inputs from txt file
# http://matplotlib.org/1.2.1/examples/pylab_examples/histogram_demo.html
# http://patorjk.com/software/taag/ -ASCII Letter Generator
# NyTIMES-https://www.nytimes.com/interactive/2017/04/02/technology/uber-drivers-psychological-tricks.html?_r=0
# This was my inspiration and genesis behind my entire idea

    
#######################################
from tkinter import *
import dataclasstypes
from dataclasstypes import Passenger,Match,Driver
import random
import shelve 
import matplotlib.pyplot as plt
from PIL import Image

####################################
# customize these functions
####################################

drivers = input("Enter the desired amount of drivers: ")
passengers = input("Enter the desired amount of passengers: ")
Match1 = Match(int(drivers), int(passengers))
Match2 = Match(int(drivers), int(passengers))
passengerPriority,driverPriority=Match1.priority()
dr_n_pas=Match1.stableMatch(driverPriority,passengerPriority)
dr_n_pas1=Match2.randomMatch()
x=Match1.match(dr_n_pas)
y=Match2.match(dr_n_pas1)

####################################
#Graphing and txt
####################################


def plot_optimal(optimal):
    dat = []
    for i in range((len(optimal)-1)): 
        dat.append(float(optimal[i]))
    print(dat)
    n,bins,patches = plt.hist(dat,10, normed=1,facecolor="green",alpha=0.75)
    plt.xlabel("average time to passenger")
    plt.ylabel("probability")
    plt.title("Distribution of Optimal Matching")
    plt.grid(True)
    plt.show()
    
def plot_optimal2(random):
    dat = []
    for i in range((len(random)-1)): 
        dat.append(float(random[i]))
    print(dat)
    n,bins,patches = plt.hist(dat,10, normed=1,facecolor="green",alpha=0.75)
    plt.xlabel("average time to passenger")
    plt.ylabel("probability")
    plt.title("Distribution of Random Matching")
    plt.grid(True)
    plt.show()
    
######################################
#Run function and init
######################################

def runSimulation():
    run(width, height)

def init(data): #initializes the key values needed in the simulation
    # load data.xyz as appropriate
    data.margin = 40
    data.cellWidth = 50
    data.cellHeight = 50
    data.rows = 15
    data.cols = 15
    data.driverRow=-1
    data.driverCol=-1
    data.passRow=-1
    data.passCol=-1
    data.gridWidth = data.cellWidth * data.rows 
    data.gridHeight = data.cellWidth * data.cols
    data.mode = "splashScreen"
    data.prevmode = "splashScreen"
    data.cellSize = data.cols // 4
    data.fontSize = 26
    data.fontSizechange = 1
    (data.prevRow, data.prevCol) = getCell(data.width // 2, data.height // 2, data)
    data.time = 0
    data.time2 = 0
    data.globalTime = Match1.globalTime
    data.timerDelay = Match1.timerDelay
    data.image = PhotoImage(file="/Users/dipakkrishnan/Dropbox/15-112/termProject/uberimage.gif")
    data.carimage = PhotoImage(file="/Users/dipakkrishnan/Dropbox/15-112/termProject/ubercarimage-2.gif")
    data.carleft = PhotoImage(file="/Users/dipakkrishnan/Dropbox/15-112/termProject/left.gif")
    data.carright = PhotoImage(file="/Users/dipakkrishnan/Dropbox/15-112/termProject/right.gif")
    data.cardown = PhotoImage(file="/Users/dipakkrishnan/Dropbox/15-112/termProject/down.gif")
    data.helpimage = PhotoImage(file="/Users/dipakkrishnan/Dropbox/15-112/termProject/helpimage.gif")
    data.cars = [data.carimage,data.carleft,data.carright,data.cardown]


####################################
# mode dispatcher #taken from 112 website # sets the linked functions
####################################

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "simulate"):   simulatemousePressed(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)
    elif (data.mode == "random"):     randommousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "simulate"):   simulatekeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)
    elif (data.mode == "random"):     randomkeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "simulate"):   simulatetimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)
    elif (data.mode == "random"):     randomtimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "simulate"):   simulateredrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)
    elif (data.mode == "random"):     randomredrawAll(canvas, data)

####################################
# splashScreen mode #taken from 112 website
####################################
def splashScreenMousePressed(event, data):
    pass

def splashScreenKeyPressed(event, data): #key press to switch modes
    if event.keysym == 'p': 
        data.mode = "simulate"
    if event.keysym == 'r':
        data.mode = "random"
    if event.keysym == 'i':
        data.prevMode = "splashScreen"
        data.mode = "help"
        
def splashScreenTimerFired(data): #this is from my hw6
    data.fontSize += 5*data.fontSizechange
    if data.fontSize > 40: #checks to make sure it doesn't get too big or small
        data.fontSizechange = -1
    if data.fontSize < 5:
        data.fontSizechange = 1

def splashScreenRedrawAll(canvas, data): #creates the splash screen w/ images
    margin = -60
    top = 10
    (left, top) = (margin, top)
    canvas.create_image(left, top, anchor=NW, image=data.image)
    canvas.create_text(data.width/2, data.height/2-20,
                       text="Optimizing the ride-sharing simulation!", 
                       font="Arial %s bold" % data.fontSize, fill="lightBlue")
    canvas.create_text(data.width/2, data.height/2+200,
                       text="Press 'p' for optimal matching,'r' for random matching, 'i' for information",
                       font="Arial 20", fill="lightBlue")

####################################
# help mode
####################################

def helpMousePressed(event, data):
    data.prevMode = "helpScreen"
    data.mode = "splashScreen"
    
def helpKeyPressed(event, data):
    pass

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data): # information about simulation
    canvas.create_rectangle(data.width,0,0,data.height,fill="black")
    margin = -60
    top = 10
    (left, top) = (margin,top)
    canvas.create_image(left, top, anchor=NW, image=data.helpimage)
    canvas.create_text(data.width//2, data.height//2,
                       text="The essential part of this simulation " + 
                       " is to show how ride-sharing solutions like Uber can be optimized. \n" +
                       "This can happen with different numbers of drivers and customers autonomously." + " You have two modes, optimal and random. \n" +" These work with different algorithms. \n"+ "They work in different times, and the graphs on the last pages show the time difference.", 
                       font="Arial 9 bold", 
                       fill = "red")
    canvas.create_text(data.width/2, data.height/2+40,
                       text="Press mouse to return to caller mode",
                             font="Arial 15", fill="red")
                        


###################################
#Grid / Simulation functions 112 website grid demo as previously referenced
###################################
def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    cellWidth  = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    row = (y - data.margin) // cellHeight
    col = (x - data.margin) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)

def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * columnWidth
    y1 = data.margin + (row+1) * columnWidth
    return (x0, y0, x1, y1)

def simulatemousePressed(event, data): #moves between different modes
    data.prevMode = "simulate"
    data.mode = "splashScreen"

def simulatekeyPressed(event, data):
    pass

def simulatetimerFired(data):
    # this calls the functions from the class to move 1 distance unit per timestep
    # also it sets passenger location for pickup and dropoff
    # works completely for any number of passengers and drivers in optimal mode
    indeed = False
    for pair in Match1.takenPairs:
        if pair[0].driverLocation != pair[0].passengerLocation:
            pair[0].timerFiredPickUp()
            if indeed == False and pair[0].globalTime % 1000 == 0: 
                Match1.time += 1
                indeed = True
        elif pair[1].location != pair[1].destination:
            pair[1].timerFiredDropOff(pair[0])
            pair[0].driverLocation = pair[1].location
            pair[0].passengerLocation = pair[1].location
            # this also handles the time, incrementing 1 second 
            if indeed == False and pair[1].globalTime%1000 == 0: 
                Match1.time += 1
                indeed = True
    

def drawCar(canvas, data):
    # this draws the car that hovers over cells in the board, using an uber car
    # icon
    radius = 5
    for pair in Match1.takenPairs:
        data.driverRow, data.driverCol = pair[0].driverLocation
        row,col=data.driverRow, data.driverCol
        (x0, y0, x1, y1) = getCellBounds(row, col, data)
        cellcx = (x0 + x1) / 2
        cellcy = (y0 + y1) / 2
        canvas.create_image(cellcx - radius, cellcy - radius, 
                        image=data.cars[pair[0].pos])

def drawPassenger(canvas, data):
    # this draws the blue dot that represents a passenger on the board
    radius = 5
    for pair in Match1.takenPairs:
        data.passRow, data.passCol = pair[1].location
        row,col=data.passRow, data.passCol
        (x0, y0, x1, y1) = getCellBounds(row, col, data)
        cellcx = (x0 + x1) / 2
        cellcy = (y0 + y1) / 2
        canvas.create_oval(cellcx - radius , cellcy - radius, 
                        cellcx + radius , cellcy + radius, 
                        fill = "blue")
        canvas.create_text(cellcx - radius + 1, cellcy-radius + 27, text=str(pair[1].destination))
        

def simulateredrawAll(canvas, data):
    canvas.create_rectangle(data.width,0,0,data.height,fill="lightBlue")
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = "lightGreen" 
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width = 15, outline = "white")
    drawPassenger(canvas, data)
    drawCar(canvas, data)
    canvas.create_text(data.width/2, data.height/2 - 310, text="Ride-Sharing Simulation!",
                       font="Arial 17 bold", fill="darkBlue")
    canvas.create_text(30,20,text = "Time:"+ str(Match1.time), fill="red")
    canvas.create_text(325,625, text="Mouse press to go back to mainscreen", fill="black")
    if Match1.final() == True: 
        average = Match1.averageTime() #computes the average time to passenger
        data.time=average
        canvas.create_text(data.width/2,data.height/2, text="Average Time to Passenger " +str(average)+" seconds", fill="blue",font="Arial 15 bold")

#####################################################
# Random Match #112 grid demo format again
#####################################################
def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (-1, -1)
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    cellWidth  = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
    row = (y - data.margin) // cellHeight
    col = (x - data.margin) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (row, col)

def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * columnWidth
    y1 = data.margin + (row+1) * columnWidth
    return (x0, y0, x1, y1)

def randommousePressed(event, data):
    data.prevMode = "random"
    data.mode = "splashScreen"

def randomkeyPressed(event, data):
    pass

def randomtimerFired(data):
    # this calls the functions from the class to move 1 distance unit per timestep
    # also it resets passenger location after pickup and dropoff so that the simulation 
    # works completely for 1 to 1 driver to passenger
    indeed=False
    for pair in Match2.takenPairs:
        if pair[0].driverLocation != pair[0].passengerLocation:
            pair[0].timerFiredPickUp()
            if indeed==False and pair[0].globalTime%1000==0: 
                Match2.time+=1
                indeed=True
        elif pair[1].location != pair[1].destination:
            pair[1].timerFiredDropOff(pair[0])
            pair[0].driverLocation = pair[1].location
            pair[0].passengerLocation = pair[1].location
            if indeed==False and pair[1].globalTime%1000==0: 
                Match2.time+=1
                indeed=True


def drawCar1(canvas,data):
    # this draws the car that hovers over cells in the board
    radius = 5
    for pair in Match2.takenPairs:
        data.driverRow, data.driverCol = pair[0].driverLocation
        row,col=data.driverRow, data.driverCol
        (x0, y0, x1, y1) = getCellBounds(row, col, data)
        cellcx = (x0 + x1) / 2
        cellcy = (y0 + y1) / 2
        canvas.create_image(cellcx - radius, cellcy - radius, 
                        image=data.cars[pair[0].pos])

def drawPassenger1(canvas, data):
    # this draws the blue dot that represents a passenger on the board
    radius = 5
    for pair in Match2.takenPairs:
        data.passRow, data.passCol = pair[1].location
        row,col=data.passRow, data.passCol
        (x0, y0, x1, y1) = getCellBounds(row, col, data)
        cellcx = (x0 + x1) / 2
        cellcy = (y0 + y1) / 2
        canvas.create_oval(cellcx - radius , cellcy - radius, 
                        cellcx + radius , cellcy + radius, 
                        fill = "blue")
        canvas.create_text(cellcx - radius + 1, cellcy-radius + 27, text=str(pair[1].destination))

def randomredrawAll(canvas, data):
    canvas.create_rectangle(data.width,0,0,data.height,fill="black")
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = "lightGreen" 
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width = 15, outline = "white")
    drawPassenger1(canvas, data)
    drawCar1(canvas, data)
    canvas.create_text(data.width/2, data.height/2 - 310, text="Ride-Sharing Simulation!",
                       font="Arial 17 bold", fill="darkBlue")
    canvas.create_text(30,20,text = "Time:"+ str(Match2.time), fill="red")
    canvas.create_text(325,625, text="Mouse press to go back to mainscreen", fill="yellow")
    if Match2.final() == True:
        average = Match2.averageTime()
        data.time2 = average
        canvas.create_text(data.width/2,data.height/2, text="Average Time to Passenger " +str(average)+" seconds", fill="red",font="Arial 15 bold")

def run(width=650, height=650):
    root = Tk()
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    # this function below works within the run function to write a text file 
    # which accumulates the average time to pas values so they can be graphed
    
    ########################
    # Write Text File
    ########################
    averagetimedata = []
    averagetimedata.append(data.time)
    with open("values.txt","a") as out_file:
        for i in range(len(averagetimedata)):
            outstring = ""
            outstring += str(averagetimedata[i])
            outstring += " "
            out_file.write(outstring)
    #########################
    # Read file and split on space
    #########################
    with open("values.txt","r") as out_file:
        #print(list(out_file.read().split(" ")))
        optimal = list(out_file.read().split(" "))
    
    ##########################
    # Write and Read Files for random mode
    ##########################
    averagetimedata2 = []
    averagetimedata2.append(data.time2)
    with open("values2.txt","a") as out_file:
        for i in range(len(averagetimedata2)):
            outstring = ""
            outstring += str(averagetimedata2[i])
            outstring += " "
            out_file.write(outstring)
    #print(averagetimedata)
    
    with open("values2.txt","r") as out_file:
        #print(list(out_file.read().split(" ")))
        random = list(out_file.read().split(" "))
        
    return(optimal,random)
       
# These last commands run the graphs and runs for random and optimal modes
y,x=run()
plot_optimal(y)
plot_optimal2(x)