import random
import sys
import time 
import threading
#this code is for use in processing
Xtiles = 30
Ytiles = 16
tilesize = 50
bombpercent = 0.15
tilelist = []
covered_tiles = []
expanded_tiles = []
flag_list = []
hold = False
Loss = False

for i in range(Xtiles*Ytiles):
  tilelist.append(0)
  covered_tiles.append(i)

#distribute bombs
for i in range(int(Xtiles*Ytiles * bombpercent)):
  bombpos = random.randint(0, Xtiles*Ytiles-1)
  while tilelist[bombpos-1] == 1:
    bombpos = random.randint(1, Xtiles*Ytiles)
  tilelist[bombpos-1] = 1
  
def monkeyBot():
    global expanded_tiles, flag_list
    def flag_pass():
        print('flagging...')
        flagged = 0
        for t in expanded_tiles:
            if bombcount(t) > 0:
                touching = get_touching_filled(t)
                if bombcount(t) == touching:
                    for i in get_touching(t):
                        if i not in flag_list and i not in expanded_tiles:
                            flagged += 1
                            print('flagged ' + str(i))
                            flag(i)
        print('flagged ' + str(flagged))
        return flagged
                
    def uncover_pass():
        print('uncovering...')
        for t in expanded_tiles:
            auto_reveal(t)
    def guess_pass():
        print('guessing...')
        best = 1
        choice = [Xtiles + 1]
        percent = 1
        for tile in expanded_tiles:
            bomb_count = bombcount(tile)
            if bomb_count == 0:
                pass
            else:
                flags = get_touching_flags(tile)
                touching = get_touching_filled(tile)
                if get_touching_filled(tile) - flags != 0:
                    print(float((bomb_count - flags))/float((get_touching_filled(tile) - flags)))
                    
                    if float((bomb_count - flags))/float((get_touching_filled(tile) - flags)) > 0:
                        percent = (bomb_count - flags)/(get_touching_filled(tile) - flags)
                    
                if percent < best:
                    best = percent
                    choice = get_touching(tile)
                else:
                    pass
        for c in choice:
            if c not in expanded_tiles and c not in flag_list:
                break
        return c
    while Loss != True:
        if flag_pass() == 0:
            #time.sleep(0.2)
            guess = guess_pass()
            print(guess)
            expand_tile(guess)
        time.sleep(0.2)
        uncover_pass()
        #time.sleep(0.2)

        
def draw_square(x,y,r,g,b):
    fill(r,g,b)
    square(x,y,tilesize)

def draw_number(count, tile):
    if count > 0:
        fill(0,0,0)
        stroke(0,0,0)
        textSize(50)
        text(str(count),((tile%Xtiles)*tilesize)+9, (tile/Xtiles+1)*tilesize-5)

def get_touching_filled(tile):
    count = 0
    for t in get_touching(tile):
        if t not in expanded_tiles:
            count += 1
    return count

def getselect():
  return int((mouseX/tilesize) + (mouseY/tilesize)*Xtiles)

def get_touching_flags(tile):
    count = 0
    for t in get_touching(tile):
        if t in flag_list:
            count += 1
    return count
def get_touching(tile):
    tiles = []
    
    #top left
    if tile - Xtiles - 1 >= 0 and tile % Xtiles != 0:
        tiles.append(tile - Xtiles - 1)
    
    #top
    if tile - Xtiles >= 0:
        tiles.append(tile - Xtiles)
    
    #top right
    if tile -Xtiles >= 0 and tile % Xtiles != Xtiles -1:
        tiles.append(tile -Xtiles + 1)
        
    #left
    if tile % Xtiles != 0:
         tiles.append(tile -1)
    
    #right
    if tile % Xtiles != Xtiles -1:
        tiles.append(tile + 1)
    
    #bottom left
    if tile + Xtiles - 1 < len(tilelist) and tile % Xtiles != 0:
        tiles.append(tile + Xtiles - 1)
        
    #bottom
    if tile + Xtiles < len(tilelist):
        tiles.append(tile + Xtiles)
        
    #bottom right
    if tile + Xtiles + 1 < len(tilelist) and tile % Xtiles != Xtiles -1:
        tiles.append(tile + Xtiles + 1)
    
    return tiles
    
def bombcount(tile):
    count = 0
    #top left
    if tile - Xtiles - 1 >= 0 and tile % Xtiles != 0:
        count += tilelist[tile - Xtiles - 1]

    #top
    if tile - Xtiles >= 0:
        count += tilelist[tile - Xtiles]
    
    #top right
    if tile -Xtiles >= 0 and tile % Xtiles != Xtiles -1:
        count += tilelist[tile -Xtiles + 1]
    
    #left
    if tile % Xtiles != 0:
         count += tilelist[tile -1]
    
    #right
    if tile % Xtiles != Xtiles -1:
        count += tilelist[tile + 1]

    #bottom left
    if tile + Xtiles - 1 < len(tilelist) and tile % Xtiles != 0:
        count += tilelist[tile + Xtiles - 1]
    
    #bottom
    if tile + Xtiles < len(tilelist):
        count += tilelist[tile + Xtiles]
    
    #bottom right
    if tile + Xtiles + 1 < len(tilelist) and tile % Xtiles != Xtiles -1:
        count += tilelist[tile + Xtiles + 1]
        
    return count

def loss():
    global loss
    loss = True
    print('loss')
    noLoop()
    fill(255,0,0)
    for y in range(0, height, tilesize):
        for x in range(0, width, tilesize):
            if tilelist[int(x/tilesize + (y/tilesize)*Xtiles)] == 1:
                square(x,y,tilesize)
def grid():
  fill(255,255,255)
  stroke(0,0,0)
  strokeWeight(2)
  for y in range(0, height, tilesize):
    for x in range(0, width, tilesize):
      square(x,y,tilesize)
      
def expand_tile(tile):
    global expanded_tiles, Loss, covered_tiles
    if tile not in expanded_tiles:
        if tile not in flag_list:
            if tilelist[tile] == 1:
                Loss = True
            else:
                expanded_tiles.append(tile)
                count = bombcount(tile)
                #draw_square((tile%Xtiles)*tilesize, (tile/Xtiles)*tilesize, 170,170,170)
                if count == 0:
                    touching = get_touching(tile)
                    for t in touching:
                        expand_tile(t)
                #else:
                    #draw_number(count, tile)
                
def auto_reveal(tile):
    if get_touching_flags(tile) == bombcount(tile):
        for t in get_touching(tile):
            if t not in flag_list:
                expand_tile(t)
def flag(tile):
    global flag_list
    if tile not in expanded_tiles:
        if tile not in flag_list:
            flag_list.append(tile)
            # fill(255, 100, 0)
            # square((tile%Xtiles)*tilesize, (tile/Xtiles)*tilesize, tilesize)
        else:
            flag_list.remove(tile)
            # fill(255,255,255)
            # square((tile%Xtiles)*tilesize, (tile/Xtiles)*tilesize, tilesize)
        
MB = threading.Thread(target=monkeyBot)
#MB.start()

def setup():
  sys.setrecursionlimit(5000)
  print(sys.getrecursionlimit())
  size(Xtiles*tilesize, Ytiles* tilesize)
  grid()

def draw():
  #draw flagged
  if Loss == True:
      loss()
  # for tile in tilelist:
  #     draw_square((tile%Xtiles)*tilesize, (tile/Xtiles)*tilesize, 255,255,255)
  for tile in expanded_tiles:
      count = bombcount(tile)
      draw_square((tile%Xtiles)*tilesize, (tile/Xtiles)*tilesize, 170,170,170)
      draw_number(count, tile)
  for tile in flag_list:
      draw_square((tile%Xtiles)*tilesize, (tile/Xtiles)*tilesize, 255,100,0)
  global hold
  #get square that is under mouse
  if mousePressed:
      if hold == False:
        index = getselect()
        if mouseButton == LEFT:
                expand_tile(index)
        elif mouseButton == RIGHT:
            flag(index)
        else:
            print('Middle')
            auto_reveal(index)
        hold = True
  else:
      hold = False
