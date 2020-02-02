import tkinter as tk
import random
import sys
import time
import highscores as hs

# global constants to seet the size of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750


#
#
#
class Player:
    def __init__(self, x_pos, y_pos):
        # character images from: https://lionheart963.itch.io/4-directional-character

        ### Action States and Player Image Creation
        self.idle_photos = []
        for i in range(4):
            self.idle_photos += [tk.PhotoImage(
                file="sprites/main_character/idle/" + str(i) + ".gif")]  # load each sprite and save in a list

        self.move_up_photos = []
        for i in range(5):
            self.move_up_photos += [tk.PhotoImage(file="sprites/main_character/move_up/" + str(i) + ".gif")]

        self.move_right_photos = []
        for i in range(6):
            self.move_right_photos += [tk.PhotoImage(file="sprites/main_character/move_right/" + str(i) + ".gif")]

        self.move_left_photos = []
        for i in range(6):
            self.move_left_photos += [tk.PhotoImage(file="sprites/main_character/move_left/" + str(i) + ".gif")]

        self.move_down_photos = []
        for i in range(5):
            self.move_down_photos += [tk.PhotoImage(file="sprites/main_character/move_down/" + str(i) + ".gif")]

        self.cut_down_photos = []
        for i in range(3):
            self.cut_down_photos += [tk.PhotoImage(file="sprites/main_character/cut_down/" + str(i) + ".gif")]

        self.action_images = {
            "idle": self.idle_photos,
            "move up": self.move_up_photos,
            "move down": self.move_down_photos,
            "move right": self.move_right_photos,
            "move left": self.move_left_photos,
            "cut down": self.cut_down_photos
        }

        self.action_state = "idle"
        self.last_state = "idle"

        self.current_photo = 0

        ### Keybindings
        win.bind('<w>', self.move_up)
        win.bind('<s>', self.move_down)
        win.bind('<a>', self.move_left)
        win.bind('<d>', self.move_right)
        win.bind('<KeyRelease>', self.release)

        ### Location States
        self.imageloc = [x_pos, y_pos]
        self.imageID = [0, 0]
        self.loc = []

    ### Display
    def display(self):
        self.imageID = canvas.create_image(self.imageloc[0], self.imageloc[1],
                                           image=self.action_images[self.action_state][self.current_photo])
        self.update_image()
        # start looping through sprites

    ### Update Image - Player
    def update_image(self):
        if s.updateState:
            if self.action_state == "move up":
                canvas.move(self.imageID, 0, -20)

            if self.action_state == "move down":
                canvas.move(self.imageID, 0, 20)

            if self.action_state == "move left":
                canvas.move(self.imageID, -20, 0)

            if self.action_state == "move right":
                canvas.move(self.imageID, 20, 0)

            if self.action_state != self.last_state:
                self.last_state = self.action_state
                self.current_photo = 0
            for each in g.room_list[g.playerloc[0]][g.playerloc[1]].cblist:
                each.checker()
            self.current_photo = (self.current_photo + 1) % len(self.action_images[self.action_state])
            canvas.itemconfig(self.imageID, image=self.action_images[self.action_state][self.current_photo])

        win.after(100, self.update_image)

    ### Keybound States
    def move_up(self, event):
        self.action_state = "move up"

    def move_down(self, event):
        self.action_state = "move down"

    def move_right(self, event):
        self.action_state = "move right"

    def move_left(self, event):
        self.action_state = "move left"

    def release(self, event):
        self.action_state = "idle"

    ### Get feet coords command - Vital
    def get_feet_coords(self):
        try:
            points = canvas.coords(self.imageID)
            feet_x = points[0]
            feet_y = points[1] + 84 / 2 - 6
            return [feet_x, feet_y]
        except IndexError:
            print(points, 'INDEX')

    ### Is In command - Vital
    def is_in(self, x_pos, y_pos):
        feet_point = self.get_feet_coords()
        feet_x = feet_point[0]
        feet_y = feet_point[1]

        ##### Feet Size
        feet_width = 50
        feet_height = 20

        ##### Determine actual collision
        return feet_x - feet_width / 2 < x_pos < feet_x + feet_width / 2 and feet_y - feet_height / 2 < y_pos < feet_y + feet_height / 2

    ### Helper methods for combat
    def is_in_combat(self, x_pos, y_pos):
        points = self.get_feet_coords()
        feet_x = points[0]
        feet_y = points[1]
        rangex = 150
        rangey = 150
        return feet_x - rangex / 2 < x_pos < feet_x + rangex / 2 and feet_y - rangey / 2 < y_pos < feet_y + rangey / 2

    def damage(self, slime):
        if slime.health == 0:
            canvas.delete(slime.slime)
            g.room_list[g.playerloc[0]][g.playerloc[1]].slime_list.remove(slime)
        else:
            slime.movestate = False
            slime.health -= 1
            slime.moveback(self.get_feet_coords()[0], self.get_feet_coords()[1])
            slime.movestate = True


#

#
class Game:
    def __init__(self):
        ### Init states of rooms - configurable
        self.size = 5
        self.room_cap = 10
        ### Other room data
        self.room_count = 0
        self.room_list = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.arch_exists = False
        ### Create Player
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        win.bind('<e>', self.combat)
        ### Init time counter
        self.tick = time.time()
        self.tock = time.time()
        ### Set up room creation
        firstrow = random.randint(0, len(self.room_list) - 1)
        firstcol = random.randint(0, len(self.room_list) - 1)
        self.playerloc = [firstrow, firstcol]
        self.room_list[firstrow][firstcol] = Room()
        self.create_rooms(firstrow + 1, firstcol)
        self.create_rooms(firstrow - 1, firstcol)
        self.create_rooms(firstrow, firstcol + 1)
        self.create_rooms(firstrow, firstcol - 1)
        self.create_arch()
        ### Intialize game
        self.display()
        self.update()
        # print(self.roomcount())

    ### Rudimentary Combat system
    def combat(self, event):
        self.player.action_state = "cut down"
        for each in self.room_list[self.playerloc[0]][self.playerloc[1]].slime_list:
            if self.player.is_in_combat(canvas.coords(each.slime)[0], canvas.coords(each.slime)[1]):
                self.player.damage(each)

    ### Arch Creation method - Makes arch in a random room from list of rooms
    def create_arch(self):
        archlist = []
        for each in self.room_list:
            for i in each:
                if type(i) == Room:
                    archlist.append(i)
        self.archroom = random.choice(archlist)
        self.archroom.make_arch()

    ### Room creation - Has a chance to create a room and if so, runs create room on nearby rooms
    def create_rooms(self, row, col):
        self.ls = [[row + 1, col], [row - 1, col], [row, col + 1], [row, col - 1]]
        if row <= len(self.room_list) - 1 and col <= len(self.room_list[row]) - 1:
            try:
                if type(self.room_list[row][col]) == Room:
                    pass
                elif self.room_cap >= self.room_count:
                    if self.room_list[row][col] == 0:
                        if random.randint(1, 2) == 1:
                            self.room_list[row][col] = Room()
                            self.room_count += 1
                            self.create_rooms(row + 1, col)
                            self.create_rooms(row - 1, col)
                            self.create_rooms(row, col + 1)
                            self.create_rooms(row, col - 1)
            except IndexError:
                return
        else:
            return

    ### Display method
    def display(self):
        self.room_list[self.playerloc[0]][self.playerloc[1]].display()
        self.player.display()
        # print(canvas.coords(self.room.arch))

    ### Game Updater - Vital
    def update(self):
        if s.updateState == True:
            ##### Edge Testing - Includes exception handling of the out of range
            try:
                if self.player.get_feet_coords()[0] >= SCREEN_WIDTH and type(
                        self.room_list[self.playerloc[0]][self.playerloc[1] + 1]) == Room:
                    ypos = self.player.get_feet_coords()[1]
                    self.room_list[self.playerloc[0]][self.playerloc[1] + 1].cblist = []
                    self.playerloc[1] += 1
                    canvas.delete("all")
                    self.player = Player(60, ypos)
                    self.display()
                elif self.player.get_feet_coords()[0] <= 0 and type(
                        self.room_list[self.playerloc[0]][self.playerloc[1] - 1]) == Room:
                    ypos = self.player.get_feet_coords()[1]
                    self.playerloc[1] -= 1
                    canvas.delete("all")
                    self.player = Player(SCREEN_WIDTH - 60, ypos)
                    self.display()
                elif self.player.get_feet_coords()[1] >= SCREEN_HEIGHT and type(
                        self.room_list[self.playerloc[0] + 1][self.playerloc[1]]) == Room:
                    xpos = self.player.get_feet_coords()[0]
                    self.playerloc[0] += 1
                    canvas.delete("all")
                    self.player = Player(xpos, 80)
                    self.display()
                elif self.player.get_feet_coords()[1] <= 0 and type(
                        self.room_list[self.playerloc[0] - 1][self.playerloc[1]]) == Room:
                    xpos = self.player.get_feet_coords()[0]
                    self.playerloc[0] -= 1
                    canvas.delete("all")
                    self.player = Player(xpos, (SCREEN_HEIGHT - 100))
                    self.display()
            except IndexError:
                print('Out of range')

            ##### Barrel Testing - smash if entered
            for each in self.room_list[self.playerloc[0]][self.playerloc[1]].barrel_list:
                if self.player.is_in(canvas.coords(each.barrel)[0],
                                     canvas.coords(each.barrel)[1] + 29) and each.barrelState == 0:
                    canvas.itemconfig(each.barrel, image=each.dec_pic[1])
                    each.barrelState = 1

            ##### Loss Testing - if is in slime
            for each in self.room_list[self.playerloc[0]][self.playerloc[1]].slime_list:
                if each.movestate:
                    each.move(self.player.get_feet_coords()[0], self.player.get_feet_coords()[1])
                if self.player.is_in(canvas.coords(each.slime)[0], canvas.coords(each.slime)[1]):
                    print('You lose!')
                    brexit()

            ##### Win Testing - if is in arch
            if self.room_list[self.playerloc[0]][self.playerloc[1]].arch_exists:
                if self.player.is_in(canvas.coords(self.room_list[self.playerloc[0]][self.playerloc[1]].arch)[0],
                                     canvas.coords(self.room_list[self.playerloc[0]][self.playerloc[1]].arch)[1] + 96):
                    print('You win!')
                    brexit()

        win.after(150, self.update)

    def roomcount(self):
        count = 0
        for each in self.room_list:
            for i in each:
                if type(i) == Room:
                    count += 1
        return count


#

### Exit Function
def brexit():
    tick = time.time() - g.tock - s.totalPauseTime
    print('You survived: ', str(int(tick)), ' seconds!')
    win.destroy()
    scoresaver()
    d = hs.Displayscores()
    sys.exit()


def scoresaver():
    infile = open('high-scores.txt', 'r+')
    tick = time.time() - g.tock - s.totalPauseTime
    lines = infile.readlines()
    newlines = []
    num = []
    dic = {}
    for each in lines:
        if each != lines[0]:
            temp = each.split(' ')
            num.append(int(temp[2]))
            newlines.append(' '.join(temp))
            try:
                if type(dic[num[-1]]) == str:
                    dic[num[-1]] = [dic[num[-1]], newlines[-1]]
                    print(dic[num[-1]])
            except KeyError:
                dic[num[-1]] = newlines[-1]
    num.append(int(tick))
    newlines.append(input('Enter Name: ') + ' - ' + str(int(tick)) + ' seconds\n')
    try:
        if type(dic[int(tick)]) == str:
            dic[int(tick)] = [dic[int(tick)], newlines[-1]]
            print(dic[num[-1]])
    except KeyError:
        dic[int(tick)] = newlines[-1]
    num.sort(reverse=True)
    infile.seek(0)
    infile.truncate(0)
    infile.write('High Scores:\n')
    for each in num:
        if len(dic[each]) > 1:
            for i in dic[each]:
                infile.write(i)
            dic[each] = ''
        else:
            infile.write(dic[each])
    infile.close()


#
class Room:
    def __init__(self):

        ### Create background tiles
        self.bg_photos = []
        for i in range(4):
            self.bg_photos += [tk.PhotoImage(file="sprites/background/ground_brown/" + str(i) + ".gif")]
        for i in range(4):
            self.bg_photos += [tk.PhotoImage(file="sprites/background/ground_green/" + str(i) + ".gif")]

        ### Create Dec's
        self.dec_list = []
        self.barrel_list = []
        class_list = [Dec, Barrel, Candle, Candelabra]
        for i in range(random.randint(2, 5)):
            choice = random.choice(class_list)
            if choice == Barrel:
                self.barrel_list.append(Barrel(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
            else:
                self.dec_list.append(choice(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))

        ### Create slimes
        self.slime_list = []
        for i in range(random.randint(2, 10)):
            self.slime_list.append(Slime(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))

        ### Init arch state
        self.arch_exists = False

        ### Create CB list
        self.cblist = []

    ### Main room display method - Vital
    def display(self):
        xpos = 0
        ypos = 0

        ### Random tiles yet, fix
        while xpos <= SCREEN_WIDTH:
            self.bg = canvas.create_image(xpos, ypos, image=random.choice(self.bg_photos))
            while ypos <= SCREEN_HEIGHT:
                self.bg = canvas.create_image(xpos, ypos, image=random.choice(self.bg_photos))
                ypos += 32
            ypos = 0
            xpos += 32

        ### Dec's, Slime's and Arch's
        for each in self.dec_list:
            each.display()
        for each in self.barrel_list:
            each.display()
        for each in self.slime_list:
            each.display()
        if self.arch_exists:
            self.arch = canvas.create_image(self.arch_loc[0], self.arch_loc[1], image=self.arch_image)
            self.cblist.append(Collision(self.cbmark1[0], self.cbmark1[1], self.cbmark1[2], self.cbmark1[3]))
            self.cblist.append(Collision(self.cbmark2[0], self.cbmark2[1], self.cbmark2[2], self.cbmark2[3]))

    ### Arch creator
    def make_arch(self):
        self.arch_image = tk.PhotoImage(file="sprites/background/full_arch/0.gif")
        self.arch_loc = [random.randint(160, SCREEN_WIDTH - 160), random.randint(192, SCREEN_HEIGHT - 192)]
        self.arch_exists = True
        self.cbmark1 = [62 + self.arch_loc[0], 80 + self.arch_loc[0], 80 + self.arch_loc[1],
                        192 / 2 + self.arch_loc[1]]
        print(self.cbmark1)
        self.cbmark2 = [-80 + self.arch_loc[0], -62 + self.arch_loc[0], 80 + self.arch_loc[1],
                        192 / 2 + self.arch_loc[1]]
        print(self.cbmark2)

#
class Collision:
    def __init__(self, xpos1, xpos2, ypos1, ypos2):
        self.xpos1 = xpos1
        self.xpos2 = xpos2
        self.ypos1 = ypos1
        self.ypos2 = ypos2

    def checker(self):
        if self.xpos1 < g.player.get_feet_coords()[0] < self.xpos2 and self.ypos1 < g.player.get_feet_coords()[0] < self.ypos2:
            if g.player.action_state == "move right":
                canvas.move(g.player.imageID, -20, 0)
            elif g.player.action_state == "move left":
                canvas.move(g.player.imageID, 20, 0)
            elif g.player.action_state == "move down":
                canvas.move(g.player.imageID, 0, -20)
            elif g.player.action_state == "move up":
                canvas.move(g.player.imageID, 0, 20)


#
class Slime:
    def __init__(self, x_pos, y_pos):

        ### Color init
        self.slime_color = random.randint(0, 7)
        self.slime_photos = []
        for i in range(6):  # 4 idle sprites
            self.slime_photos += [tk.PhotoImage(file="sprites/slimes/" + str(self.slime_color) + "/move/" + str(
                i) + ".gif")]  # load each sprite and save in a list

        ### Set states and random speed
        self.slime_number = random.randint(0, len(self.slime_photos) - 1)
        self.imageloc = [x_pos, y_pos]
        self.speed = random.randint(1, 10)
        self.slimeup = False
        self.health = 5
        self.movestate = True

    ### Display function - Could use polishing. Slime up isn't needed
    def display(self):
        self.slime = canvas.create_image(self.imageloc[0], self.imageloc[1], image=self.slime_photos[self.slime_number])
        if not self.slimeup:
            self.update_image()
            self.slimeup = True

    ### Updater
    def update_image(self):
        if s.updateState:
            self.slime_number = (self.slime_number + 1) % len(self.slime_photos)
            canvas.itemconfig(self.slime, image=self.slime_photos[self.slime_number])
        win.after(100, self.update_image)

    ### Main move method - Vital
    def move(self, x_pos, y_pos):
        cur_x = canvas.coords(self.slime)[0]
        cur_y = canvas.coords(self.slime)[1]
        self.total_distance = ((x_pos - cur_x) ** 2 + (y_pos - cur_y) ** 2) ** 0.5
        self.x_dis = ((x_pos - cur_x) / self.total_distance) * self.speed
        self.y_dis = ((y_pos - cur_y) / self.total_distance) * self.speed
        canvas.move(self.slime, self.x_dis, self.y_dis)

    def moveback(self, x_pos, y_pos):
        cur_x = canvas.coords(self.slime)[0]
        cur_y = canvas.coords(self.slime)[1]
        self.total_distance = ((x_pos - cur_x) ** 2 + (y_pos - cur_y) ** 2) ** 0.5
        self.x_dis = -2 * ((x_pos - cur_x) / self.total_distance) * self.speed
        self.y_dis = -2 * ((y_pos - cur_y) / self.total_distance) * self.speed
        canvas.move(self.slime, self.x_dis, self.y_dis)
    #


#

#
class Dec:
    def __init__(self, xpos, ypos):

        ### Dic for Dec's. Could use polishing
        dec_ls = ['grass', 'pillar', 'pots', 'rock', 'rug']
        dec_dic = {
            'grass': 2,
            'pillar': 2,
            'rock': 4,
            'pots': ['red', 'green'],
            'rug': ['blue', 'brown', 'green', 'red']
        }
        choice1 = random.choice(dec_ls)

        ### Image Loader based on random choice
        if type(dec_dic[choice1]) == list:
            choice2 = random.choice(dec_dic[choice1])
            if choice1 == 'pots':
                self.dec_pic = []
                for i in range(3):
                    self.dec_pic += [
                        tk.PhotoImage(file="sprites/background/" + choice1 + "/" + choice2 + '/' + str(i) + ".gif")]
            else:
                self.dec_pic = []
                for i in range(2):
                    self.dec_pic += [
                        tk.PhotoImage(file="sprites/background/" + choice1 + "/" + choice2 + '/' + str(i) + ".gif")]
        else:
            self.dec_pic = []
            for i in range(dec_dic[choice1]):
                self.dec_pic += [tk.PhotoImage(file="sprites/background/" + choice1 + "/" + str(i) + ".gif")]

        self.imageLoc = [xpos, ypos]

    ### Displayer
    def display(self):
        self.dec = canvas.create_image(self.imageLoc[0], self.imageLoc[1], image=random.choice(self.dec_pic))


#

#
class Barrel:
    def __init__(self, xpos, ypos):
        self.dec_pic = []
        for i in range(2):
            self.dec_pic += [tk.PhotoImage(file="sprites/background/barrel/" + str(i) + ".gif")]
        self.barrelState = random.randint(0, 1)
        self.imageLoc = [xpos, ypos]

    def display(self):
        self.barrel = canvas.create_image(self.imageLoc[0], self.imageLoc[1], image=self.dec_pic[self.barrelState])


#

#
class Candelabra:
    def __init__(self, xpos, ypos):
        self.dec_pic = []
        for i in range(3):
            self.dec_pic += [tk.PhotoImage(file="sprites/background/candelabra/" + str(i) + ".gif")]
        self.abraState = random.randint(0, 2)
        self.imageLoc = [xpos, ypos]

    def display(self):
        self.candelabra = canvas.create_image(self.imageLoc[0], self.imageLoc[1], image=self.dec_pic[self.abraState])
        self.update_image()

    def update_image(self):
        if s.updateState:
            self.abraState = (self.abraState + 1) % len(self.dec_pic)
            canvas.itemconfig(self.candelabra, image=self.dec_pic[self.abraState])
        win.after(150, self.update_image)


#

#
class Candle:
    def __init__(self, xpos, ypos):
        self.dec_pic = []
        for i in range(3):
            self.dec_pic += [tk.PhotoImage(file="sprites/background/candle/" + str(i) + ".gif")]
        self.canState = random.randint(0, 2)
        self.imageLoc = [xpos, ypos]

    def display(self):
        self.candle = canvas.create_image(self.imageLoc[0], self.imageLoc[1], image=self.dec_pic[self.canState])
        self.update_image()

    def update_image(self):
        if s.updateState:
            self.canState = (self.canState + 1) % len(self.dec_pic)
            canvas.itemconfig(self.candle, image=self.dec_pic[self.canState])
        win.after(150, self.update_image)


#

### HUD GUI
class Gui:
    def __init__(self):
        c2.create_line(0, 1, SCREEN_WIDTH - 1, 1, width=25)
        c2.create_line(0, SCREEN_HEIGHT / 4 - 1, SCREEN_WIDTH - 1, SCREEN_HEIGHT / 4 - 1, width=25)
        c2.create_line(3 * SCREEN_WIDTH / 4, 0, 3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4 - 1, width=20)
        c2.create_line(SCREEN_WIDTH - 11, 0, SCREEN_WIDTH - 11, SCREEN_HEIGHT / 4 - 1, width=20)
        c2.create_line(11, 0, 11, SCREEN_HEIGHT / 4 - 1, width=20)

    def create_blip(self, x, y):
        return


#
#
#

### Win Init        
win = tk.Tk()
win.minsize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
win.maxsize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT * 2)
win.title("The Dungeon Master")

timeLabel = tk.Label(win, text=str(0))


def timeUpdate():
    if s.updateState:
        timeLabel['text'] = str(int(time.time() - g.tock - s.totalPauseTime))
    win.after(100, timeUpdate)


timeLabel.grid()
### Main Page Init
canvas = tk.Canvas(win, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.grid()

### HUD Init
c2 = tk.Canvas(win, width=SCREEN_WIDTH, height=SCREEN_HEIGHT / 4)
c2.grid()


### Pause - Tracks a state and applies it across the program
class State:
    def __init__(self):
        self.updateState = False
        self.totalPauseTime = 0
        self.tick = time.time()

    def getState(self):
        return self.updateState

    def changeState(self):
        if self.updateState:
            self.updateState = False
            self.tick = time.time()
        else:
            self.totalPauseTime += time.time() - self.tick
            self.updateState = True


s = State()


def pause(event):
    s.changeState()


### Termination Command - Key bound to delete

win.bind('<Escape>', pause)
win.bind('<Delete>', brexit)

### Game Start
g = Game()
p = Gui()
timeUpdate()
tk.mainloop()
