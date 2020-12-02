from tkinter import Tk, Canvas, PhotoImage
from tkinter import E, W, Entry, NW
from random import randint as rand, sample
from time import sleep
import os

# resolution of screen is 1280x720 for best view
# cheat key makes upper traingles disappear
# boss key can be used when your superior
# comes near your screen


# Core functions that create main screens
def create_window(h, w):
    window = Tk()
    window.title("Jump Game")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w,  h,  x,  y))
    return window


def create_menu():
    global state

    if(gamesavecheck()):
        continuefill = textfill
    else:
        continuefill = "black"

    canvas.delete("all")
    state = "menu"
    starty = startby - buttonh/2
    endy = startby + buttonh/2
    startx = width/2 - buttonw/2
    endx = width/2 + buttonw/2

    # shapes of buttons
    buttonback = []
    for i in range(5):
        buttonback.append(canvas.create_oval(startx,  starty,
                          endx,  endy,  fill=buttonfill))
        starty += distanceby
        endy += distanceby
    x = width/2
    y = startby
    canvas.create_text(x,  y,  text="Continue",  fill=continuefill,
                       font="Times 30 italic bold")
    y += distanceby
    canvas.create_text(x,  y,  text="New Game",  fill=textfill,
                       font="Times 30 italic bold")
    y += distanceby
    canvas.create_text(x,  y,  text="Setting",  fill=textfill,
                       font="Times 30 italic bold")
    y += distanceby
    canvas.create_text(x,  y,  text="Leaderboard",  fill=textfill,
                       font="Times 30 italic bold")
    y += distanceby
    canvas.create_text(x,  y,  text="Exit",  fill=textfill,
                       font="Times 30 italic bold")
    y += distanceby


# reads the location of traingles and player. Then recreate the game
# that is saved. Score and boost level is saved to recreate game
# exactly as it saved.
def continue_game():
    global traingles,  player,  score,  state,  pausemenu,  scoregame,  boost

    state = "game"
    canvas.delete("all")

    states["cheat"] = False
    savedfile = open("saved.txt", "r")

    savedfile.readline()

    saved_score = savedfile.readline()
    saved_score = saved_score.split(":")[1][:-1]
    scoregame = int(saved_score)

    savedfile.readline()

    playerUpper = float(savedfile.readline().split(":")[1][:-1])
    playerDown = float(savedfile.readline().split(":")[1][:-1])

    boost = int(savedfile.readline().split(":")[1][:-1])
    savedfile.readline()

    savedtraingle = []

    for i in range(10):
        savedtraingle.append(savedfile.readline())

    savedfile.close()
    deletesave()

    canvas.create_line(width, margin, 0, margin, fill=shapefill)
    canvas.create_line(width, height-margin, 0, height - margin,
                       fill=shapefill)
    scoretxt = "Score: "+str(scoregame)
    score = canvas.create_text(width/2, 20, text=scoretxt, fill=textfill,
                               font=" Times 20 italic bold")

    canvas.create_oval(width - margin + pausepad, pausepad,
                       width-pausepad, margin-pausepad, fill=shapefill)
    pausel1 = canvas.create_line(width - margin/2, pausepad + 4,
                                 width - margin/2, margin-pausepad-4,
                                 fill="black", width=3)
    pausel2 = canvas.create_line(width - margin/2, pausepad + 4,
                                 width - margin/2, margin-pausepad-4,
                                 fill="black", width=3)
    canvas.move(pausel1, -5, 0)
    canvas.move(pausel2, 5, 0)

    pausemenu = []
    pausemenu.append(canvas.create_oval(width - margin + pausepad,
                     pausepad,  width - pausepad,  margin - pausepad,
                     fill=shapefill))
    radius = (margin - pausepad*2) / 2
    radius -= 3
    points = [width, margin/2, width - radius, margin/2 - radius,
              width - radius, margin/2+radius]
    pausemenu.append(canvas.create_polygon(points, fill="black"))
    canvas.move(pausemenu[1], -10, 0)

    temp = canvas.create_oval(width - margin - buttonw/2 - pausepad,
                              pausepad, width-margin-pausepad,
                              margin-pausepad, fill=buttonfill)
    pausemenu.append(temp)
    temp = canvas.create_text(width - margin - buttonw/4 - pausepad,
                              margin/2, text="save&quit", fill=textfill,
                              font="Times 20 italic bold")
    pausemenu.append(temp)

    # moves continue button and save&exit button beyond screen so user
    # wouldn't see.
    for thing in pausemenu:
        canvas.move(thing, 0, -100)

    traingles = continueTraingle(savedtraingle)

    player = canvas.create_rectangle(width/2-player_size/2, playerUpper,
                                     width/2+player_size/2, playerDown,
                                     fill=playerfill)

    movtraingle()

    canvas.pack()


def create_new_game():
    global traingles, player, score, state, pausemenu

    state = "game"
    canvas.delete("all")
    deletesave()

    canvas.create_line(width, margin, 0, margin, fill=shapefill)
    canvas.create_line(width, height-margin, 0, height-margin,
                       fill=shapefill)
    scoretxt = "Score: "+str(scoregame)
    score = canvas.create_text(width/2, 20, text=scoretxt,
                               fill=textfill, font=" Times 20 italic bold")

    canvas.create_oval(width-margin+pausepad,  pausepad,  width-pausepad,
                       margin-pausepad,  fill=shapefill)
    pausel1 = canvas.create_line(width-margin/2, pausepad+4, width-margin/2,
                                 margin-pausepad-4, fill="black", width=3)
    pausel2 = canvas.create_line(width-margin/2, pausepad+4, width-margin/2,
                                 margin-pausepad-4, fill="black", width=3)
    canvas.move(pausel1, -5, 0)
    canvas.move(pausel2, 5, 0)

    pausemenu = []
    pausemenu.append(canvas.create_oval(width-margin+pausepad,  pausepad,
                                        width-pausepad,  margin-pausepad,
                                        fill=shapefill))
    radius = (margin-pausepad*2)/2
    radius -= 3
    points = [width, margin/2, width-radius, margin/2-radius, width-radius,
              margin/2+radius]
    pausemenu.append(canvas.create_polygon(points, fill="black"))
    canvas.move(pausemenu[1], -10, 0)

    pausemenu.append(canvas.create_oval(width-margin-buttonw/2-pausepad,
                     pausepad, width-margin-pausepad, margin-pausepad,
                     fill=buttonfill))
    pausemenu.append(canvas.create_text(width-margin-buttonw/4-pausepad,
                     margin/2, text="save&quit", fill=textfill,
                     font="Times 20 italic bold"))

    for thing in pausemenu:
        canvas.move(thing, 0, -100)

    # at any given moment there will be 10 traingle. 5 on top and 5 on bottom
    traingles = generate_traingle(canvas, height, width, margin)

    player = canvas.create_rectangle(width/2-player_size/2,
                                     height/2-player_size/2,
                                     width/2+player_size/2,
                                     height/2+player_size/2,
                                     fill=playerfill)

    movtraingle()

    canvas.pack()


def setting():
    global state, rectanglew, rectangleh, text1set
    rectanglew = 100
    rectangleh = 40
    state = "setting"
    canvas.delete("all")

    y = 40
    canvas.create_oval(width/2-buttonw/2-100,
                       y-buttonh/2, width/2-100,
                       y+buttonh/2, fill=buttonfill)
    canvas.create_text(width/2, y, text="Settings",
                       font="Times 40 italic bold",
                       fill=textfill)
    canvas.create_text(width/2-160, y, text="Back",
                       font="Times 30 italic bold",
                       fill=textfill)
    textset = []        # text to indicate which setting player changing
    rectangles = []
    # text to indicate what is currect setting and changes to <key>
    # when changing
    text1set = []
    for name in keyname:
        y += 100
        textset.append(canvas.create_text(width/2-30, y,
                                          text=name.capitalize(),
                                          fill=textfill, anchor=E,
                                          font="Times 30 italic bold"))
        rectangles.append(canvas.create_rectangle(width/2, y-rectangleh/2,
                                                  width/2+rectanglew,
                                                  y+rectangleh/2,
                                                  fill="#f0efeb"))
        text1set.append(canvas.create_text(width/2+rectanglew/2, y,
                                           fill="black",
                                           font="Times 20 italic bold",
                                           text=keys[name]))


def leaderboard():
    global state
    state = "leader"
    canvas.delete("all")
    y = 40
    canvas.create_oval(width/2-buttonw/2-170, y-buttonh/2, width/2-170,
                       y+buttonh/2, fill=buttonfill)
    canvas.create_text(width/2, y, text="Leaderboard",
                       font="Times 40 italic bold",
                       fill=textfill)
    canvas.create_text(width/2-230, y, text="Back",
                       font="Times 30 italic bold",
                       fill=textfill)
    leaderboardcreate(100)


# functions related to obstacle traingle
def generate_traingle_pos(h, w, margin, start):

    space_margin = 50

    # following section uses score to decide space between traingles
    # to change level of the game
    if(scoregame <= 5):
        space = 150
    elif(scoregame <= 10):
        space = 120
    elif(scoregame <= 20):
        space = 90
    else:
        space = 70

    upper = margin+space_margin+space/2
    lower = h-upper
    x = rand(upper, lower)
    sizeup = x-space/2-margin
    sizedown = h-x-space/2-margin
    points = [[start-sizeup/2, margin, start+sizeup/2, margin,
              start, x-space/2], [start-sizedown/2, h-margin,
              start+sizedown/2, h-margin, start, x+space/2]]
    return points


# this function creates new 2 traingle behind last traingle
# when leftest traingles go beyond the screen
def keeptraingle():
    global traingles

    canvas.pack()
    pos = canvas.coords(traingles[0][0])
    x = pos[4]
    if x < -200:
        for n in range(2):
            canvas.delete(traingles[0][n])
        del traingles[0]
        pos1 = canvas.coords(traingles[len(traingles)-1][0])
        x1 = pos1[4]
        traingleAddPos = generate_traingle_pos(height, width, margin,
                                               x1+traingle_space)
        if(states["cheat"]):
            traingleUp = canvas.create_polygon(traingleAddPos[0],
                                               fill=bgfill)
        else:
            traingleUp = canvas.create_polygon(traingleAddPos[0],
                                               fill=shapefill)
        traingleDown = canvas.create_polygon(traingleAddPos[1],
                                             fill=shapefill)
        canvas.tag_lower(traingleUp)
        canvas.tag_lower(traingleDown)
        traingles.append([traingleUp, traingleDown])


def continueTraingle(info):
    tra = []
    position = []
    for i in range(5):
        position.append([])
        for n in range(2):
            position[i].append([])
            pos = info.pop(0)
            pos = pos.split("|")[:-1]
            for thing in pos:
                position[i][n].append(float(thing))
    for i in range(5):
        tra.append([])
        for n in range(2):
            tra[i].append(canvas.create_polygon(position[i][n],
                          fill=shapefill))
            canvas.tag_lower(tra[i])
    return tra


# this function is responsible or moving traingles and player
# during whole game
def movtraingle():
    global boost, counter, states, scoregame, space, finalscore
    counter += 1
    canvas.pack()

    keeptraingle()

    if (boost > 0):
        boost -= 2
        canvas.move(player, 0, -2)
    else:
        canvas.move(player, 0, 2)

    for i in range(len(traingles)):
        if(find_active_traingle(i)):
            fail = collision(player, traingles[i][0], traingles[i][1])
            if (fail):
                states["failed"] = True
    if(canvas.coords(player)[1] <= margin or
       canvas.coords(player)[3] >= (height-margin)):
        states["failed"] = True

    if (states["failed"]):
        canvas.create_image(width/2, height/2, image=game_over)
        window.update()
        sleep(2)
        finalscore = scoregame
        gamedelete()
        gameoverpage()
        return 0
    for i in range(len(traingles)):
        for n in range(2):
            canvas.move(traingles[i][n], -2, 0)
        if(canvas.coords(traingles[i][0])[4] == width/2):
            scoregame += 1
            txt = "Score: "+str(scoregame)
            canvas.itemconfig(score, text=txt)
    if(counter % 50 == 0):
        for i in range(len(sparks)):
            canvas.delete(sparks[i])
        sparks.clear()
        counter = 0
    for i in range(len(sparks)):
        canvas.move(sparks[i], rand(-1, 0), rand(0, 1))

    if(states["pause"]):
        window.after(10, pauseGame)
    else:
        window.after(10, movtraingle)


def generate_traingle(canvas, height, width, margin):
    traingle_number = 5
    start_pos = 1000
    traingles = []
    for i in range(traingle_number):
        pos = generate_traingle_pos(height, width, margin, start_pos)
        traingle_up = canvas.create_polygon(pos[0], fill=shapefill)
        traingle_down = canvas.create_polygon(pos[1], fill=shapefill)
        canvas.tag_lower(traingle_up)
        canvas.tag_lower(traingle_down)
        traingles.append([traingle_up, traingle_down])
        start_pos += traingle_space
    return traingles


# instead of checking all traingle for collision. only traingle that is
# on right side of player need to be checked for collision
def find_active_traingle(i):
    check1 = canvas.coords(traingles[i][0])[0] <= (width/2+player_size/2)
    check2 = canvas.coords(traingles[i][0])[4] >= (width/2+player_size/2)
    check1 = check1 and check2
    check3 = canvas.coords(traingles[i][1])[0] <= (width/2+player_size/2)
    check4 = canvas.coords(traingles[i][1])[4] >= (width/2+player_size/2)
    check3 = check3 and check4
    return check1 or check3


# leaderboard related functions
def saveleader(board):
    leader = open("leader.txt", "w")
    txt = ""
    for namescore in board:
        txt += namescore[0]+":"+str(namescore[1])+"\n"
    leader.write(txt)


# reads saved leaderboard file and return leaderbaord in list
def leader():
    lboard = []
    try:
        leader = open("leader.txt", "r")
        for i in range(5):
            namescore = leader.readline()[:-1].split(":")
            lboard.append([namescore[0], int(namescore[1])])
    except Exception:
        leader = open("leader.txt", "w")
        txt = ""
        for i in range(5):
            txt += "----------:0\n"
            lboard.append(["----------", 0])
        leader.write(txt)
        leader.close()
    return lboard


# arrange players relative to their score
# same scored players will be arranged
# depending on which one added first
def arrangeboard():
    global lboard
    arrange = lboard
    newlist = []
    while len(arrange) > 0:
        max = -1
        maxloc = -1
        for i in range(len(arrange)):
            if(arrange[i][1] > max):
                max = arrange[i][1]
                maxloc = i
        newlist.append(arrange[maxloc])
        del arrange[maxloc]
    if(len(newlist) > 5):
        del newlist[5]
        lboard = newlist
    else:
        lboard = newlist


def leaderboardcreate(y):
    y1 = y
    for i in range(3):
        y1 += 70
        canvas.create_image(width/2-300, y1, image=medals[i], anchor=E)
    for i in range(len(lboard)):
        y += 70
        txt = str(i+1)+"."+lboard[i][0]
        x = width/2-300
        canvas.create_text(x, y, anchor=W, font="Times 30 italic bold",
                           fill=textfill, text=txt)
        txt = str(lboard[i][1])
        canvas.create_text(width/2, y, anchor=W, font="Times 30 italic bold",
                           fill=textfill, text=txt)


def addscore():
    global lboard
    canvas.focus_set()
    name = nameask.get()
    lboard.append([name, finalscore])
    arrangeboard()
    leaderboard()


# game save and delete save
def gamesave():
    savefile = open("saved.txt", "w")
    txt = "Saved\n"
    txt += "score:"+str(scoregame)
    txt += '\n'
    txt += "player info"
    txt += '\n'
    playerpos = canvas.coords(player)
    txt += "upper:"+str(playerpos[1])
    txt += '\n'
    txt += "lower:"+str(playerpos[3])
    txt += '\n'
    txt += "boost:"+str(boost)
    txt += '\n'
    txt += "traingles:\n"
    for i in range(len(traingles)):
        for up_or_down in range(2):
            trainglepos = canvas.coords(traingles[i][up_or_down])
            for n in range(6):
                txt += str(trainglepos[n])+'|'
            txt += "\n"
    savefile.write(txt)
    savefile.close()


def deletesave():
    try:
        os.remove("saved.txt")
    except Exception:
        pass


# cheat key and boss key things
def cheat_thing():
    for i in range(len(traingles)):
        if(states["cheat"]):
            canvas.itemconfig(traingles[i][0], fill=bgfill)
        else:
            canvas.itemconfig(traingles[i][0], fill=shapefill)


def boss_activate():
    global states, excel
    states["pause"] = True
    states["boss"] = True
    excel = canvas.create_image(0, 0, anchor=NW, image=excel_screen)


def boss_deactivate():
    global states
    states["pause"] = False
    states["boss"] = False
    canvas.delete(excel)


# mouse click and key click detection
def keyclicked(event):
    global boost, keys, settingkey, states
    if(event.keysym == keys["jump"] and not states["failed"]
       and state == "game" and not states["pause"]):
        boost = 70
        for i in range(len(sparks)):
            canvas.delete(sparks[i])
        sparks.clear()
        sprakling()
    elif(event.keysym == keys["cheat"] and not states["failed"]
         and state == "game" and not states["pause"]):
        if not states["cheat"]:
            states["cheat"] = True
            cheat_thing()
        else:
            states["cheat"] = False
            cheat_thing()
    elif(event.keysym == keys["boss"]):
        if not states["boss"]:
            boss_activate()
        else:
            boss_deactivate()

    if(settingkey != "nope"):
        for i in range(len(keyname)):
            if settingkey == keyname[i]:
                keys[settingkey] = event.keysym
                canvas.itemconfig(text1set[i], text=event.keysym)
                settingkey = "nope"


# using global state variable to keep track of which
# page user is on. Thus, program can know which regions
# of page is buttons.
def clickmouse(event):
    global states
    x = event.x
    y = event.y
    if(state == "menu"):
        startx = width/2-buttonw/2
        endx = width/2+buttonw/2

        starty = startby-buttonh/2
        endy = startby+buttonh/2

        if(x > startx and x < endx and y > starty and y < endy and
           states["saved_file"]):
            continue_game()
        starty += distanceby
        endy += distanceby
        if(x > startx and x < endx and y > starty and y < endy):
            create_new_game()
        starty += distanceby
        endy += distanceby
        if(x > startx and x < endx and y > starty and y < endy):
            setting()
        starty += distanceby
        endy += distanceby
        if(x > startx and x < endx and y > starty and y < endy):
            leaderboard()
        starty += distanceby
        endy += distanceby
        if(x > startx and x < endx and y > starty and y < endy):
            window.destroy()
    elif(state == "game"):
        if(x > (width-margin) and y < margin):
            if not states["pause"]:
                states["pause"] = True
            else:
                states["pause"] = False
        elif(x > (width-margin-buttonw/2) and x < (width-margin)
             and y < margin and states["pause"]):
            gamesave()
            gamedelete()
            create_menu()
    elif(state == "setting"):
        if(x > (width/2-buttonw/2-100) and x < (width/2-100) and
           y > (40-buttonh/2) and y < (40+buttonh/2)):
            create_menu()
        else:
            if(x > width/2 and x < (width/2+rectanglew)):
                yset = 40
                for name in keyname:
                    yset += 100
                    if(y > (yset-rectangleh/2) and y < (yset+rectangleh/2)):
                        settingchange(name)
    elif(state == "leader"):
        if(x > (width/2-buttonw/2-170) and x < (width/2-170) and
           y > (40-buttonh/2) and y < (40+buttonh/2)):
            create_menu()
    elif(state == "gameover"):
        if(x > (width/2+200) and x < (width/2+200+buttonw/2) and
           y > (140-buttonh/2) and y < (140+buttonh/2)):
            addscore()


def settingchange(name):
    global settingkey
    canvas.itemconfig(text1set[keyname.index(name)], text="<click>")
    settingkey = name


# collision detections uses fact that traingles' height and
# base is same length. Additionally, player not moving horizontally.
# this codes only compare left side of traingle with right most
# locations of player
def collision(player, traingleUp, traingleDown):
    canvas.pack()
    playerPos = canvas.coords(player)
    traingleUpPos = canvas.coords(traingleUp)
    traingleDownpos = canvas.coords(traingleDown)

    x1 = traingleUpPos[0]
    x1 -= playerPos[2]

    # when cheat is on. upper traingle shouldn't appear
    if (x1 <= 0 and not states["cheat"]):
        dieZoneUp = margin-x1*2
    else:
        dieZoneUp = margin
    x2 = traingleDownpos[0]
    x2 -= playerPos[2]
    if(x2 <= 0):
        dieZoneDown = height-(margin-x2*2)
    else:
        dieZoneDown = height-margin
    if(playerPos[1] <= dieZoneUp or playerPos[3] >= dieZoneDown):
        return True
    else:
        return False


# creates sprakles near bottom left to
# make impression that boost is making
# player go up.
def sprakling():
    pos = canvas.coords(player)
    x = pos[0]
    y = pos[3]
    sizes = [4, 2]
    color = ["#ffadad", "#ffd6a5", "#fdffb6", "#caffbf",
             "#9bf6ff", "#a0c4ff", "#bdb2ff", "#fffffc"]
    for i in range(25):
        y_move = rand(1, 20)
        x_move = rand(1, 20)
        size = sample(sizes, 1)[0]
        filling = sample(color, 1)[0]
        sparks.append(canvas.create_oval(x-x_move-size, y+y_move,
                                         x-x_move, y+y_move+size,
                                         fill=filling))


# this will keep screen frozen and allow user to save&quit or
# continue game
def pauseGame():
    global states
    if not states["pause_change"]:
        for thing in pausemenu:
            canvas.move(thing, 0, 100)
    states["pause_change"] = True
    if not states["pause"]:
        for thing in pausemenu:
            canvas.move(thing, 0, -100)
        states["pause_change"] = False
        window.after(10, movtraingle)
    else:
        window.after(10, pauseGame)


# this page will ask user for their name and
# add it to leaderboard
def gameoverpage():
    global nameask, state
    state = "gameover"
    canvas.delete("all")
    y = 40
    nameask = Entry(canvas)
    canvas.create_text(width/2, y, text="Leaderboard",
                       font="Times 40 italic bold",
                       fill=textfill)
    y += 100
    canvas.create_text(width/2-280, y, anchor=W, text="Name:",
                       font="Times 30 italic bold", fill=textfill)
    canvas.create_window(width/2, y, window=nameask, anchor=E)
    txt = "Score:"+str(finalscore)
    canvas.create_text(width/2+30, y, anchor=W,
                       font="Times 30 italic bold",  text=txt,
                       fill=textfill)
    canvas.create_oval(width/2+200, y-buttonh/2, width/2+200+buttonw/2,
                       y+buttonh/2, fill=buttonfill)
    canvas.create_text(width/2+200+buttonw/4, y, text="Add",
                       fill=textfill,
                       font="Times 30 italic bold")
    leaderboardcreate(150)


# putting starting values into variables.
def gamedelete():
    global boost, scoregame, states, traingles
    states["pause"] = False
    boost = 0
    scoregame = 0
    states["failed"] = False
    traingles.clear()


def gamesavecheck():
    global states
    try:
        savedfile = open("saved.txt", "r")
        savedfile.close()
        states["saved_file"] = True
        return True
    except Exception:
        states["saved_file"] = False
        return False


boost = 0       # keep track of how much up motion left
counter = 0     # used to know when to delete sparklings
scoregame = 0


startby = 120       # vertical location of the upmost button
distanceby = 100    # distance between buttons
buttonw = 240       # width of button
buttonh = 60        # height of button

keys = {"jump": "space", "boss": "b", "cheat": "c"}
keyname = ["jump", "boss", "cheat"]


# codes of colors used
buttonfill = "#e76f51"
textfill = "#caf0f8"
shapefill = "#90e0ef"
playerfill = "#fdffb6"
bgfill = "#264653"


# all global variable used to keep track of
# what is happening in game.
settingkey = "nope"
state = "menu"
states = {"failed": False, "pause": False,
          "pause_change": False, "saved_file": False,
          "cheat": False, "boss": False}


traingle_space = 500
width = 1280      # screen
height = 720      # screen
margin = 40       # top and bottom margin of game
player_size = 30
sparks = []

# space between 2 traingles nearest
# point (changes as game progress)
space = 150


pausepad = 4    # padding of pause button

window = create_window(height, width)
canvas = Canvas(window, bg=bgfill, width=width, height=height)
canvas.focus_set()
canvas.bind('<Key>',  keyclicked)
canvas.bind('<Button-1>',  clickmouse)

# boss key screen. (My own screenshot)
excel_screen = PhotoImage(file="excel.gif")

# Design by macrovector / Freepik
medals = []
medals.append(PhotoImage(file="gold.gif"))
medals.append(PhotoImage(file="silver.gif"))
medals.append(PhotoImage(file="bronze.gif"))

# Design by Eightonesix / Freepik
game_over = PhotoImage(file="game_over.gif")

lboard = leader()
create_menu()
canvas.pack()


window.mainloop()
saveleader(lboard)
