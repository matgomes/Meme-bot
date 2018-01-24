from ast import literal_eval as make_tuple
from PIL import Image
import random
import json
import os


home_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = home_dir + '\\Templates\\'
source_dir = home_dir + '\\Source\\'
memes_dir = home_dir + '\\Memes\\'
meme_log = home_dir + '\\log'

with open('sizes.json') as sizes:
    jsonData = json.load(sizes)

secure_random = random.SystemRandom()

# Random template
rand_temp = secure_random.choice(os.listdir(temp_dir))
# Get template number, eliminates file extension
temp_num = rand_temp.split('.')[0]
# Template
temp = Image.open(temp_dir + rand_temp)
# Contains background color and box sizes
tempInfo = jsonData[temp_num]
# Background colour
bg_color = tempInfo['background']

# b - black
if bg_color == 'b' :
    colour = 0
# w - white
elif bg_color == 'w' :
    colour = (255, 255, 255, 0)

# o - over (pasted over image, no bg)
if bg_color != 'o' :
    backg = Image.new('RGB', temp.size, colour)
else :
    backg = temp

# Counter for boxes
n = 0
# Gets all source images to be used in template (makes sure it's not a duplicated meme)
while True :
    source_imgs = []

    for box in tempInfo['boxes'] :
        # If image is repeated, no need to get another random src_img
        if 'repeat_prev' not in tempInfo['boxes'][n] :
            # Random source image (e.g. '98.png')
            rand_source = secure_random.choice(os.listdir(source_dir))
            source_index = rand_source.split('.')[0]
        # Random source index (e.g. '98')
        source_imgs.append(source_index)

        n += 1

    # Name for the file
    meme_name = temp_num + '-' + '-'.join(source_imgs) + '.png'

    # If meme duplicated, runs loop again (gets different src images)
    with open(meme_log) as log :
        for line in log :
            if meme_name in line :
                break
        else :
            break

n = 0

while n < len(source_imgs) :
    # Blank Area Properties
    size = make_tuple(tempInfo['boxes'][n]['size'])
    size_x = size[0]
    size_y = size[1]

    # source image
    src = Image.open(source_dir + source_imgs[n] + '.png')

    # Resizes image AND keeps aspect ratio
    ## Shrink
    if src.size[0] > size_x or src.size[1] > size_y :
        src.thumbnail((size_x,size_y), Image.LANCZOS)
    ## Enlarge
    else :
        hpercent = (size_y / float(src.size[1])) #Magic pt. 1
        wsize = int((float(src.size[0]) * float(hpercent))) #Magic 2: The Awakening
        src = src.resize((wsize, size_y)) #Magic 3: Revenge of the Syntax

        if src.size[0] > size_x  :
            wpercent = (size_x / float(src.size[0])) #Magic IV: A New Hope
            hsize = int((float(src.size[1]) * float(wpercent))) #Magic 5: Wrath of Fam
            src = src.resize((size_x, hsize)) #Magic 6: The Return of the Bug

    # Coordinates of top left corner (where image is pasted)
    top_left = make_tuple(tempInfo['boxes'][n]['left_corner'])
    paste_x = top_left[0]
    paste_y = top_left[1]

    # Source Image Width
    width = src.size[0]
    height = src.size[1]
    # Blank Area - Source Image Width
    black_x = size_x - width
    black_y = size_y - height
    # Pastes centered Source Image in Template
    backg.paste(src, (int(paste_x + black_x/2), int(paste_y + black_y/2)))
    # Goes to next source image (if there is a space for it)
    n += 1

# Puts Template on top of background (when bg_col = b/w)
if tempInfo['background'] != 'o' :
    backg.paste(temp, (0,0), temp)
# Saves meme
backg.save(memes_dir + meme_name)
