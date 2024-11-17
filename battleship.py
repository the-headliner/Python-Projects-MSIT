
"""
Battleship Project
Name: Laxmikant Vishwakarma
Roll No:2023501089
"""
import battleship_tests as test
project = "Battleship" # don't edit this
### SIMULATION FUNCTIONS ###
from tkinter import *
import random
EMPTY_UNCLICKED = 1       #Blue APS
SHIP_UNCLICKED = 2        #Yellow APS
EMPTY_CLICKED = 3        #White APS
SHIP_CLICKED = 4        #Red ASP
'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):   # All my helping data is stored here in makeModel (Data storage)::Data structure
    data["Num_rows"]=10    #Data for number of rows canvas should have ["Num_row"] is the key and 10 is the value
    data["Num_Cols"]=10    #Data for number of columns canvas should have ["Num_cols"] is the key and 10 is the value
    data["Board_size"]=500  #The board size for both user&comp should be 500.
    x= data["Num_rows"]   #data["Num_rows"] stored in a variable x i.e x=10
    data["Cell_size"]= data["Board_size"]//x
    data["numShips"]=5   #Number of ships we need in the board of user
    data["User_Board"]=emptyGrid(data["Num_rows"],data["Num_Cols"]) #This is userboard data which gets constructed with the help of emptygrid function
    data["Computer_Board"] =emptyGrid(data["Num_rows"],data["Num_Cols"])
    data["Computer_Board"]=addShips(data["Computer_Board"],data["numShips"])
    #data["User_Board"]=addShips(data["User_Board"],data["numShips"])
    data["temp"]=[]
    data["current_ships"]=0   #this is my usership tracker
    data["TurnAsofnow"]=0    #present number of turns taken
    data["MaxAllowedturns"]=50   #maximum number of turn allowed to be palyed on board.
    data["Winner"]=None    #As of now we have -"No Winner"
    return None

'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, compCanvas,data["Computer_Board"], True)
    drawGrid(data, userCanvas,data["User_Board"], True)
    drawShip(data,userCanvas,data["temp"]) 
    drawGameOver(data,userCanvas)  
    return 

'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym=="Return":
        makeModel(data)
    pass

'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["Winner"]==None:
        a=getClickedCell(data,event)
        if board=="user":                  #If the board is of user and action is being performed in that.
            clickUserBoard(data,a[0],a[1])  
            if data["current_ships"]==5:   #If the count of current_ship has reached to 5 then return. NO furthur action reqd
                return
                
        if board=="comp" and data["current_ships"]==5: #if the board is of computer and action being in that.
            runGameTurn(data,a[0],a[1])                #Can start the game!
#### STAGE 1 ####
'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
# Here we are creating an empty grid i.e. creating a cell structure board from scratch.
def emptyGrid(rows, cols):  #This function takes rows and cols and returns a 2D list.
    main_lst=[]  #this is my final 2D list which will be returned.
    for _ in range(rows):  #running a loop
        sub_lst=[]   #this is my intermediary list(1D list)
        for _ in range(cols):  
            sub_lst.append(EMPTY_UNCLICKED)  #the list will be appended with Empty unclicked i.e 1.(Blue)
        main_lst.append(sub_lst)    # now main_lst will be a collection of sub_lsts.
    return main_lst   #returning the mai_lst.
#print(emptyGrid(8,8))
'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    coordinates_of_ship=[]  # This 2D list will contain the coordinates where our ship has to be onboarded.
    #Let computer set coordinates for our ship randomly so that we have a ship on board in our matrix.
    Row_Index=random.randint(1,8)  # Randomly choose a row number in [1-8] range.
    Column_Index=random.randint(1,8) #Randomly choose a column number in [1-8] range.
    flip_choice=random.randint(0,1) # Now based on Flip choice , decide if the Ship will be vertically placed or horizontally:
    if flip_choice==0:
        coordinates_of_ship=[[Row_Index-1,Column_Index],[Row_Index,Column_Index],[Row_Index+1,Column_Index]]  # Ship is placed Vertical
    elif flip_choice==1:
        coordinates_of_ship=[[Row_Index,Column_Index-1],[Row_Index,Column_Index],[Row_Index,Column_Index+1]]
    
    return coordinates_of_ship  #return a newly formed coordinates.
'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for check1 in range(len(grid)):
        for check2 in range(len(grid[0])):
            if grid[check1][check2]==SHIP_UNCLICKED and [check1,check2] in ship:
                return False
    return True
'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    ship_count=0
    while True:
        ship=createShip()
        if checkShip(grid,ship)==True:
            ship_count+=1
            for i in ship:
                a=i[0]
                b=i[1]
                grid[a][b]=SHIP_UNCLICKED
            if ship_count==numShips:
                break
    return grid
'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            c=data["Cell_size"]
            x1=j*c
            y1=i*c
            x2=x1+c
            y2=y1+c
            if showShips==False:
                color="blue"
                if grid[i][j]==SHIP_CLICKED:
                    color="Red"
                if grid[i][j]==EMPTY_CLICKED:
                    color="white"
            elif grid[i][j]==SHIP_UNCLICKED:
                    color="Yellow"
            elif grid[i][j]==EMPTY_UNCLICKED:
                    color="Blue"
            elif grid[i][j]==SHIP_CLICKED:
                color="Red"
            elif grid[i][j]==EMPTY_CLICKED:
                    color="white"
            canvas.create_rectangle(x1,y1,x2,y2,fill=color)
    return 

#store data about the board dimensions.

   #return
### STAGE 2 ###
'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1]==ship[1][1]==ship[2][1] and ship[0][0]+1==ship[1][0]==ship[2][0]-1:
        return True
    return False
'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0]==ship[1][0]==ship[2][0] and ship[0][1]+1==ship[1][1]==ship[2][1]-1:
        return True
    return False
   
'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    list=[]
    y=event.y//data["Cell_size"]
    list.append(y)
    x=event.x//data["Cell_size"]
    list.append(x)
    return list

'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i,j in ship:
        x0,y0=j*data["Cell_size"],i*data["Cell_size"]
        x1,y1=x0+data["Cell_size"],y0+data["Cell_size"]
        color="white"
        canvas.create_rectangle(x0,y0,x1,y1,fill=color)
    return

'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid,ship)==True:
        if isVertical(ship)==True or isHorizontal(ship)==True:
            return True
    return False

'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    grid=data["User_Board"]
    ship=data["temp"]
    if shipIsValid(grid,ship):
        data["current_ships"]+=1
        for k in ship:
            row,col=k
            grid[row][col]=SHIP_UNCLICKED
    data["temp"]=[]       
    return
'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
   if data["current_ships"]==data["numShips"]:
    return
   if [row,col] in data["temp"]:
    return
   userboard=data["User_Board"]
   if userboard[row][col]!=1:
    return
   else:
    data["temp"].append([row,col])

   if len(data["temp"])==3:
    placeShip(data)
   return
### STAGE 3 ###
'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
   
        if board[row][col]==SHIP_UNCLICKED:   #Its YEllow as of now!
            board[row][col]=SHIP_CLICKED  #It needs to become as red (as we have detected the ship)
            if isGameOver(board)==True:
                data["Winner"]=player
        elif board[row][col]==EMPTY_UNCLICKED:  #Its Blue:(water) as of now!   [Signifying a grid cell]
            board[row][col]=EMPTY_CLICKED    # It needs to become white signifying ::(As target missed)
            
            if isGameOver(board)==True:
                data["Winner"]=player
        return
'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["Computer_Board"][row][col]==SHIP_CLICKED or  data["Computer_Board"][row][col]==EMPTY_CLICKED:
       # data["TurnAsofnow"]+=1
        return
    else:
        updateBoard(data,data["Computer_Board"],row,col,"user")
        #data["TurnAsofnow"]+=1
    [row,col]=getComputerGuess(data["User_Board"])
    
    updateBoard(data,data["User_Board"],row,col,"comp")
    data["TurnAsofnow"]+=1   #Incrementing the no. of turn after both have made their moves!
    if data["TurnAsofnow"]==data["MaxAllowedturns"]:
        data["Winner"]="Draw"
    return

'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while True:
        row=random.randint(0,9)
        col=random.randint(0,9)
        if board[row][col]==SHIP_UNCLICKED:
            return [row,col]
        elif board[row][col]==EMPTY_UNCLICKED:
            return [row,col]
    return

'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]==SHIP_UNCLICKED:
                return False
    return True
'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["Winner"]=="user":
        canvas.create_text(250,250,text="Congo",font=("Arial",24),fill="Black")
        canvas.create_text(250,300,text="press enter to play again",font=("Arial",14),fill="Black")
      
    elif data["Winner"]=="comp":
        canvas.create_text(250,50,text="You Lost",font=("Arial",24),fill="Black")
        canvas.create_text(350,100,text="press enter to play again",font=("Arial",14),fill="Black")
    elif data["Winner"]=="Draw":
        canvas.create_text(250,50,text="You are out of Moves!",font=("Arial",24),fill="Black")
        canvas.create_text(350,100,text="Press enter to Play again",font=("Arial",14),fill="Black")
        return
### SIMULATION FRAMEWORK ###
from tkinter import *
def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()
def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)
def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)
def runSimulation(w, h):
    data = { }
    makeModel(data)
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()
    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()
    makeView(data, userCanvas, compCanvas)
    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))
    updateView(data, userCanvas, compCanvas)
    root.mainloop()

### RUN CODE ###
# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " STAGE 1 TESTS " +  "#" * 16 + "\n")
    # test.stage1Tests()
    ## Uncomment these for STAGE 2 ##
    print("\n" + "#"*15 + " STAGE 2 TESTS " +  "#" * 16 + "\n")
    test.stage2Tests()

    ## Uncomment these for STAGE 3 ##
    
    print("\n" + "#"*15 + " STAGE 3 TESTS " +  "#" * 16 + "\n")
    test.stage3Tests()
    
    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
