import tkinter as tk
import random
import sys
import time
# global constants to set the size of the screen - feel free to update!
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750                        


#
#
#
class Player:
    def __init__(self,x_pos,y_pos):
        # character images from: https://lionheart963.itch.io/4-directional-character
        # create lists of PhotoImages for each animation
        self.idle_photos = []
        for i in range(4): # 4 idle sprites
            self.idle_photos += [tk.PhotoImage(file="sprites/main_character/idle/"+str(i)+".gif")] # load each sprite and save in a list
        
        self.move_up_photos = []
        for i in range(5): # 5 moving up sprites
            self.move_up_photos += [tk.PhotoImage(file="sprites/main_character/move_up/"+str(i)+".gif")] 

        ### TODO WARMUP 2 step 1: load photos for moving other directions
        # Note: up and down have 5 sprites, left and right have 6! Look into the sprites folder if you want to check.
        self.move_right_photos = []
        for i in range(6):
            self.move_right_photos += [tk.PhotoImage(file="sprites/main_character/move_right/"+str(i)+".gif")]

        self.move_left_photos = []
        for i in range(6):
            self.move_left_photos += [tk.PhotoImage(file="sprites/main_character/move_left/"+str(i)+".gif")]

        self.move_down_photos = []
        for i in range(5):
            self.move_down_photos += [tk.PhotoImage(file="sprites/main_character/move_down/"+str(i)+".gif")] 


        # dictionary to map current "action" to images
        self.action_images = {
            "idle":self.idle_photos,
            "move up":self.move_up_photos,
            "move down":self.move_down_photos,
            "move right":self.move_right_photos,
            "move left":self.move_left_photos
        } ### TODO WARMUP 2 step 2: add photos for other actions 


        # keep track of current and previous action state!
        self.action_state = "idle"
        self.last_state   = "idle"
        
        self.current_photo = 0 # start at the first photo

        # bind up and release keys - 'w' also works if you want to use 'wasd' controls
        win.bind('<w>',self.move_up)
        
        ### TODO WARMUP 2 step 4 (make the functions first, so you have something to bind to!): bind other keys

        win.bind('<s>',self.move_down)
        win.bind('<a>',self.move_left)
        win.bind('<d>',self.move_right)
        win.bind('<e>',self.printslime)
        win.bind('<Escape>',self.kill)
        win.bind('<KeyRelease>',self.release) # checking for any key release, not quite right but will work for us

        # first image
        self.imageloc = [x_pos,y_pos]
        self.imageID = [0,0]
        self.loc = []
    def display(self):
        self.imageID = canvas.create_image(self.imageloc[0],self.imageloc[1],image=self.action_images[self.action_state][self.current_photo])
        self.update_image()
        # start looping through sprites

    def kill(self,event):
        win.destroy()
        sys.exit()
    # used to move sprite and rotate through sprites to create animation
    def update_image(self):
        # move sprite on the screen according to current state (if "idle", doesn't have to move)

        if self.action_state == "move up": # moves the character up if state is "move up"
            canvas.move(self.imageID,0,-20) # Tkinter's top left is (0,0) and down is positive, so moving up means going negative in the y direction
            
        ### TODO WARMUP 2 step 5: move for other actions states

        if self.action_state == "move down": # moves the character up if state is "move up"
            canvas.move(self.imageID,0,20)

        if self.action_state == "move left": # moves the character up if state is "move up"
            canvas.move(self.imageID,-20,0)

        if self.action_state == "move right": # moves the character up if state is "move up"
            canvas.move(self.imageID,20,0)



        # rotates through photos to animate, resets animation on state change
        if self.action_state != self.last_state: # don't reset photos unless changing state
            self.last_state = self.action_state
            self.current_photo = 0 # go back to beginning of animation

        self.current_photo = (self.current_photo+1) % len(self.action_images[self.action_state]) # go to the next photo, wrap back to 0 if at end
        canvas.itemconfig(self.imageID, image=self.action_images[self.action_state][self.current_photo]) # update photo
        win.after(100, self.update_image) # automatically calls itself every 150ms
        
    def printslime(self,event):
        print(g.room_list[g.playerloc[0]][g.playerloc[1]].slime_list[0].speed)
        print(g.room_list[g.playerloc[0]][g.playerloc[1]].slime_list[0].total_distance)
        print(g.room_list[g.playerloc[0]][g.playerloc[1]].slime_list[0].x_dis)
        print(g.room_list[g.playerloc[0]][g.playerloc[1]].slime_list[0].y_dis)
        
    # set the state to the up action state, "move up"
    def move_up(self,event):
        self.action_state = "move up"

    ### TODO WARMUP 2 step 3: create functions for the other movements
    def move_down(self,event):
        self.action_state = "move down"

    def move_right(self,event):
        self.action_state = "move right"

    def move_left(self,event):
        self.action_state = "move left"

    # when a button is released, go back to idle action state, "idle"
    def release(self, event):
        self.action_state = "idle"

    # returns the x,y of the center of the feet as a list - not being used yet!
    def get_feet_coords(self):
        try:
            points = canvas.coords(self.imageID) # gets x and y position of the center of the image
            feet_x = points[0]  
            feet_y = points[1] + 84/2 - 6 # image is 84 pixels tall but the feet don't reach the bottom so there's an offset
            return [feet_x,feet_y]
        except IndexError:
            print(points, 'INDEX')
    
    # takes in an x and y position and returns True if that point
    # is in the Player feet area, otherwise returns False - also not being used yet!
    def is_in(self, x_pos, y_pos):
        # get center of bottom of feet
        feet_point = self.get_feet_coords()

        # remove x and y positions for easy access
        feet_x = feet_point[0]
        feet_y = feet_point[1]

        # determine size of player feet rectangle, finetuned to what felt right
        # feel free to adjust once you're using this!
        feet_width = 50
        feet_height = 20 

        # determine actual collision
        return feet_x - feet_width/2 < x_pos < feet_x + feet_width/2 and feet_y - feet_height/2 < y_pos < feet_y + feet_height/2
#
#
#



#
#
#
class Game:
    def __init__(self):
        # create player
        self.size = 5
        self.room_cap = 10
        self.room_count = 0
        self.room_list = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.arch_exists = False
        self.player = Player(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.tick = time.time()
        self.tock = time.time()
        firstrow = random.randint(0,len(self.room_list)-1)
        firstcol = random.randint(0,len(self.room_list)-1)
        self.playerloc = [firstrow,firstcol]
        self.room_list[firstrow][firstcol] = Room()
        self.create_rooms(firstrow+1,firstcol)
        self.create_rooms(firstrow-1,firstcol)
        self.create_rooms(firstrow,firstcol+1)
        self.create_rooms(firstrow,firstcol-1)
        self.create_arch()
        self.display()
        self.update()
        print(self.roomcount())
        
    def create_arch(self):
        archlist = []
        for each in self.room_list:
            for i in each:
                if type(i) == Room:
                    archlist.append(i)
        self.archroom = random.choice(archlist)
        self.archroom.make_arch()
        
    def create_rooms(self,row,col):
        self.ls = [[row+1,col],[row-1,col],[row,col+1],[row,col-1]]
        if row <= len(self.room_list)-1 and col <= len(self.room_list[row])-1:
            #print(row,col,'WTF')
            if type(self.room_list[row][col]) == Room:
                pass
            elif self.room_cap >= self.room_count:
                if self.room_list[row][col] == 0:
                    if random.randint(1,2) == 1:
                        self.room_list[row][col] = Room()
                        self.room_count += 1
                        self.create_rooms(row+1,col)
                        self.create_rooms(row-1,col)
                        self.create_rooms(row,col+1)
                        self.create_rooms(row,col-1)
        else:
            return
                    
    def display(self):
        self.room_list[self.playerloc[0]][self.playerloc[1]].display()
        self.player.display()
        #print(canvas.coords(self.room.arch))
        
    def update(self):
        #print(self.player.get_feet_coords())
        try:
            if self.player.get_feet_coords()[0] >= SCREEN_WIDTH and type(self.room_list[self.playerloc[0]][self.playerloc[1]+1]) == Room:
                xpos = self.player.get_feet_coords()[0]
                ypos = self.player.get_feet_coords()[1]
                self.playerloc[1] += 1
                canvas.delete("all")
                self.player = Player(60,ypos)
                self.display()
            elif self.player.get_feet_coords()[0] <= 0 and type(self.room_list[self.playerloc[0]][self.playerloc[1]-1]) == Room:
                xpos = self.player.get_feet_coords()[0]
                ypos = self.player.get_feet_coords()[1]
                self.playerloc[1] -= 1
                canvas.delete("all")
                self.player = Player(SCREEN_WIDTH-60,ypos)
                self.display()
            elif self.player.get_feet_coords()[1] >= SCREEN_HEIGHT and type(self.room_list[self.playerloc[0]+1][self.playerloc[1]]) == Room:
                xpos = self.player.get_feet_coords()[0]
                ypos = self.player.get_feet_coords()[1]
                self.playerloc[0] += 1
                canvas.delete("all")
                self.player = Player(xpos,80)
                self.display()
            elif self.player.get_feet_coords()[1] <= 0 and type(self.room_list[self.playerloc[0]-1][self.playerloc[1]]) == Room:
                xpos = self.player.get_feet_coords()[0]
                ypos = self.player.get_feet_coords()[1]
                self.playerloc[0] -= 1
                canvas.delete("all")
                self.player = Player(xpos,(SCREEN_HEIGHT-100))
                self.display()
        except IndexError:
            print('Out of range')
        for each in self.room_list[self.playerloc[0]][self.playerloc[1]].barrel_list:
            if self.player.is_in(canvas.coords(each.barrel)[0],canvas.coords(each.barrel)[1]+29) and each.barrelstate == 0:
                canvas.itemconfig(each.barrel, image=each.dec_pic[1])
        for each in self.room_list[self.playerloc[0]][self.playerloc[1]].slime_list:
            each.move(self.player.get_feet_coords()[0],self.player.get_feet_coords()[1])
            if self.player.is_in(canvas.coords(each.slime)[0],canvas.coords(each.slime)[1]):
                print('You lose!')
                brexit()
        if self.room_list[self.playerloc[0]][self.playerloc[1]].arch_exists == True:
            if self.player.is_in(canvas.coords(self.room_list[self.playerloc[0]][self.playerloc[1]].arch)[0],canvas.coords(self.room_list[self.playerloc[0]][self.playerloc[1]].arch)[1]+96):
                print('You win!')
                brexit()
        self.tick = time.time()-self.tock
        win.after(150, self.update)

    def roomcount(self):
        count = 0
        for each in self.room_list:
            for i in each:
                if type(i) == Room:
                    count += 1
        return count
#
#
#

def brexit():
    print('You survived: ',str(int(g.tick)),' seconds!')
    print('press enter to exit')
    win.destroy()
    sys.exit()

#
#
#
class Room:
    def __init__(self):
        self.bg_photos = []
        for i in range(4): # 4 idle sprites
            self.bg_photos += [tk.PhotoImage(file="sprites/background/ground_brown/"+str(i)+".gif")] # load each sprite and save in a list
        for i in range(4): # 4 idle sprites
            self.bg_photos += [tk.PhotoImage(file="sprites/background/ground_green/"+str(i)+".gif")] # load each sprite and save in a list
        self.dec_list = []
        self.barrel_list = []
        class_list = [Dec, Barrel, Candle, Candelabra]
        for i in range(random.randint(2,5)):
            choice = random.choice(class_list)
            if choice == Barrel:
                self.barrel_list.append(Barrel(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT)))
            else:
                self.dec_list.append(choice(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT)))
        self.slime_list = []
        for i in range(random.randint(2,10)):
            self.slime_list.append(Slime(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT)))
        self.arch_exists = False
    def display(self):
        xpos=0
        ypos=0
        while xpos <= SCREEN_WIDTH:
            self.bg = canvas.create_image(xpos,ypos,image=random.choice(self.bg_photos))
            while ypos <= SCREEN_HEIGHT:
                self.bg = canvas.create_image(xpos,ypos,image=random.choice(self.bg_photos))
                ypos += 32
            ypos=0
            xpos += 32
        for each in self.dec_list:
            each.display()
        for each in self.barrel_list:
            each.display()
        for each in self.slime_list:
            each.display()
        if self.arch_exists == True:
            self.arch = canvas.create_image(self.arch_loc[0],self.arch_loc[1],image=self.arch_image)
            
    def make_arch(self):
        self.arch_image = tk.PhotoImage(file="sprites/background/full_arch/0.gif")
        self.arch_loc = [random.randint(160,SCREEN_WIDTH-160),random.randint(192,SCREEN_HEIGHT-192)]
        self.arch_exists = True
#
#
#



#
#
#
class Slime:
    def __init__(self,x_pos,y_pos):
        self.slime_color = random.randint(0,7)
        self.slime_photos = []
        for i in range(6): # 4 idle sprites
            self.slime_photos += [tk.PhotoImage(file="sprites/slimes/"+str(self.slime_color)+"/move/"+str(i)+".gif")] # load each sprite and save in a list
        self.slime_number = random.randint(0,len(self.slime_photos)-1)
        self.imageloc = [x_pos,y_pos]
        self.speed = random.randint(1,10)
        self.slimeup = False
        
    def display(self):
        self.slime = canvas.create_image(self.imageloc[0],self.imageloc[1],image=self.slime_photos[self.slime_number])
        if self.slimeup == False:
            self.update_image()
            self.slimeup = True
            
    def update_image(self):
        self.slime_number = (self.slime_number+1) % len(self.slime_photos) # go to the next photo, wrap back to 0 if at end
        canvas.itemconfig(self.slime, image=self.slime_photos[self.slime_number]) # update photo
        win.after(100, self.update_image)

    def move(self, x_pos, y_pos):
        cur_x = canvas.coords(self.slime)[0]
        cur_y = canvas.coords(self.slime)[1]
        self.total_distance = ((x_pos-cur_x)**2+(y_pos-cur_y)**2)**0.5
        self.x_dis = ((x_pos-cur_x)/self.total_distance)*self.speed
        self.y_dis = ((y_pos-cur_y)/self.total_distance)*self.speed
        canvas.move(self.slime,self.x_dis,self.y_dis)
        
#
#
#



#
#
#
class Dec:
    def __init__(self,xpos,ypos):
        dec_ls = ['grass','pillar','pots','rock','rug']
        dec_dic = {
            'grass':2,
            'pillar':2,
            'rock':4,
            'pots':['red','green'],
            'rug':['blue','brown','green','red']
            }
        choice1 = random.choice(dec_ls)
        if type(dec_dic[choice1]) == list:
            choice2 = random.choice(dec_dic[choice1])
            if choice1 == 'pots':
                self.dec_pic = []
                for i in range(3):
                    self.dec_pic += [tk.PhotoImage(file="sprites/background/"+choice1+"/"+choice2+'/'+str(i)+".gif")]
            else:
                self.dec_pic = []
                for i in range(2):
                    self.dec_pic += [tk.PhotoImage(file="sprites/background/"+choice1+"/"+choice2+'/'+str(i)+".gif")]
        else:
            self.dec_pic = []
            for i in range(dec_dic[choice1]):
                self.dec_pic += [tk.PhotoImage(file="sprites/background/"+choice1+"/"+str(i)+".gif")]
        self.imageloc = [xpos,ypos]
    def display(self):
        self.dec = canvas.create_image(self.imageloc[0],self.imageloc[1],image=random.choice(self.dec_pic))
#
#
#



#
#
#
class Barrel:
    def __init__(self, xpos, ypos):
        self.dec_pic = []
        for i in range(2):
            self.dec_pic += [tk.PhotoImage(file="sprites/background/barrel/"+str(i)+".gif")]
        self.barrelstate = random.randint(0,1)
        self.imageloc = [xpos,ypos]
        
    def display(self):
        self.barrel = canvas.create_image(self.imageloc[0],self.imageloc[1],image=self.dec_pic[self.barrelstate])
#
#
#



#
#
#
class Candelabra:
    def __init__(self, xpos, ypos):
        self.dec_pic = []
        for i in range(3):
            self.dec_pic += [tk.PhotoImage(file="sprites/background/candelabra/"+str(i)+".gif")]
        self.abrastate = random.randint(0,2)
        self.imageloc = [xpos,ypos]

    def display(self):
        self.candelabra = canvas.create_image(self.imageloc[0],self.imageloc[1],image=self.dec_pic[self.abrastate])
        self.update_image()
        
    def update_image(self):
        self.abrastate = (self.abrastate+1) % len(self.dec_pic) # go to the next photo, wrap back to 0 if at end
        canvas.itemconfig(self.candelabra, image=self.dec_pic[self.abrastate]) # update photo
        win.after(150, self.update_image)
#
#
#



#
#
#
class Candle:
    def __init__(self, xpos, ypos):
        self.dec_pic = []
        for i in range(3):
            self.dec_pic += [tk.PhotoImage(file="sprites/background/candle/"+str(i)+".gif")]
        self.canstate = random.randint(0,2)
        self.imageloc = [xpos,ypos]
    
    def display(self):
        self.candle = canvas.create_image(self.imageloc[0],self.imageloc[1],image=self.dec_pic[self.canstate])
        self.update_image()
        
    def update_image(self):
        self.canstate = (self.canstate+1) % len(self.dec_pic) # go to the next photo, wrap back to 0 if at end
        canvas.itemconfig(self.candle, image=self.dec_pic[self.canstate]) # update photo
        win.after(150, self.update_image)
#
#
#

class Gui:
    def __init__(self):
        c2.create_line(0,1,SCREEN_WIDTH-1,1,width=25)
        c2.create_line(0,SCREEN_HEIGHT/4-1,SCREEN_WIDTH-1,SCREEN_HEIGHT/4-1,width=25)
        c2.create_line(3*SCREEN_WIDTH/4,0,3*SCREEN_WIDTH/4,SCREEN_HEIGHT/4-1,width=20)
        c2.create_line(SCREEN_WIDTH-11,0,SCREEN_WIDTH-11,SCREEN_HEIGHT/4-1,width=20)
        c2.create_line(11,0,11,SCREEN_HEIGHT/4-1,width=20)

    def create_blip(self,x,y):
        return

#
#
#
# Normally we say not to use global variables, but graphics programming often uses them
# to keep track of various states and information more easily. They are okay here.

win = tk.Tk()
win.minsize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
win.maxsize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT*2)
win.title("The Dungeon Master")
canvas = tk.Canvas(win, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.grid()
c2 = tk.Canvas(win, width=SCREEN_WIDTH, height=SCREEN_HEIGHT/4)
c2.grid()
g = Game() # need to save to a vaiable, otherwise images sometimes vanish
p = Gui()
#tk.mainloop()
