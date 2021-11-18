from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import rsa

global path_image
imgToDecode_Size = 250, 250

def on_click():
    global path_image
    path_image = filedialog.askopenfilename()
    # load the image using the path
    load_image = Image.open(path_image)
    # set the image into the GUI and adjust size
    load_image.resize(imgToDecode_Size, Image.ANTIALIAS)
    load_image.thumbnail(imgToDecode_Size, Image.ANTIALIAS)
    # load the image as a numpy array for efficient computation and change the type to unsigned integer
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(app, image=render)
    img.image = render
    #This op in the x part is for the image to be centered everytime
    img.place(x=167 - load_image.width/2, y=60)

def xor(key, data):
    #Create list where we'll append the new message
    newData = []
    for (elemK, elemD) in zip(key, data):
        replace = ''
        for (numK, numD) in zip(elemK, elemD):
            if(numK == '0' and numD == '0'):
                replace = replace + '0'
            elif(numK == '0' and numD == '1'):
                replace = replace + '1'
            elif(numK == '1' and numD == '0'):
                replace = replace + '1'
            elif(numK == '1' and numD == '1'):
                replace= replace + '0'
        newData.append(replace)

    #Since our key was shorter, we need to append the missing elements in data to our new message
    for elem in data[len(key):]:   
        newData.append(elem)

    return newData

def decrypt(keyToDecode):
    # load the image and convert it into a numpy array 
    load = Image.open(path_image)
    load.thumbnail(imgToDecode_Size, Image.ANTIALIAS)
    load = np.asarray(load)
    load = Image.fromarray(np.uint8(load))
    render = ImageTk.PhotoImage(load)
    img = Label(app, image=render)
    img.image = render

    # Algorithm to decrypt the data from the image
    img = cv2.imread(path_image)
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if(stop):
            break

    message = []
    # join all the bits to form letters (ASCII Representation)
    for i in range(int((len(data)+1)/8)):
        message.append(data[i*8:(i*8+8)])

    key = keyToDecode.get(1.0, "end-1c")
    key = [format(ord(i), '08b') for i in key]
    message = xor(key, message)
    # join all the letters to form the message.
    message = [chr(int(''.join(i), 2)) for i in message]
    message = ''.join(message)

    message_label = Label(app, text=message, bg='white', font=("Times New Roman", 14))
    message_label.place(x=610, y=70)

# INTERFACE
app = Tk()
app.configure(background='#A069D6')
app.title("Steganography App")
app.geometry('975x400')

myFont = font.Font(weight="bold", size=10)
myFontTlt = font.Font(weight="bold", size=25)

lbl_Title1 = Label(app,text="Decode", bg='#A069D6', font=myFontTlt, padx=10, pady=5)
lbl_Title1.place(anchor=NW)

upload_btn1 = Button(app, text="Upload Image", bg='#35D3A7', fg='white', relief=RAISED, bd=3, pady= 3, padx = 3, font=myFont, command=on_click) #8D41D6
upload_btn1.place(x=117, y=320)

lbl_txtEncode = Label(app,text="Mensaje oculto", bg='#A069D6', font=myFont)
lbl_txtEncode.place(x=475, y=82)
txtToEncode = Text(app, wrap=WORD, width=30)
txtToEncode.place(x=605, y=65, height=50)

lbl_keyEncode = Label(app,text="Clave para desencriptar", bg='#A069D6', font=myFont)
lbl_keyEncode.place(x=440, y=147)
keyToEncode = Text(app, wrap=WORD, width=30)
keyToEncode.place(x=605, y=130, height=50)

decrypt_btn = Button(app, text="Decode", bg='#35D3A7', fg='white', relief=RAISED, bd=3, pady= 3, padx = 3, font=myFont, command= lambda: decrypt(keyToEncode))
decrypt_btn.place(x=698, y=200)

app.mainloop()
