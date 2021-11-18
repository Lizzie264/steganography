from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math

global path_image
imgToEncode_Size = 250, 250

def on_click():
    global path_image
    path_image = filedialog.askopenfilename()
    # load the image using the path
    load_image = Image.open(path_image)
    # set the image into the GUI and adjust size
    load_image.resize(imgToEncode_Size, Image.ANTIALIAS)
    load_image.thumbnail(imgToEncode_Size, Image.ANTIALIAS)
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

def encrypt_data_into_image(textToHide, keyToEncode, nameToEncode):
    global path_image
    data = textToHide.get(1.0, "end-1c")
    key = keyToEncode.get(1.0, "end-1c")
    key = [format(ord(i), '08b') for i in key]
    print(key)
    # load the image
    img = cv2.imread(path_image)
    # Get image into ASCII FORMAT
    data = [format(ord(i), '08b') for i in data]
    print(data)

    # Here we do an xor for encryption
    data = xor(key, data)

    # Operations required to know until which row we must hide data
    _, width, _ = img.shape
    PixReq = len(data) * 3

    RowReq = PixReq/width
    RowReq = math.ceil(RowReq)

    count = 0
    charCount = 0
    
    #Traversing in each row and checking cases to know when to modify the less significant bit
    for i in range(RowReq + 1):
        while(count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            
            for index_k, k in enumerate(char):
                if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if(index_k % 3 == 2): #A letter was already encoded, keep track of it
                    count += 1
                if(index_k == 7): #Check if we should stop encoding
                    if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if(charCount*3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0

    # Write the encrypted image into a new file
    #cv2.imwrite("encrypted_image.png", img)
    cv2.imwrite(nameToEncode.get(1.0, "end-1c"), img)

    success_label = Label(app, text="Encryption Successful!", bg='#8D41D6', font=myFontTlt)
    success_label.place(x=525, y=300)

# INTERFACE
app = Tk()
app.configure(background='#35D3A7')
app.title("Steganography App")
app.geometry('975x400')

myFont = font.Font(weight="bold", size=10)
myFontTlt = font.Font(weight="bold", size=25)

lbl_Title1 = Label(app,text="Encode", bg='#35D3A7', font=myFontTlt, padx=10, pady=5)
lbl_Title1.place(anchor=NW)

upload_btn1 = Button(app, text="Upload Image", bg='#8D41D6', fg='white', relief=RAISED, bd=3, pady= 3, padx = 3, font=myFont, command=on_click) #8D41D6
upload_btn1.place(x=117, y=320)

lbl_txtEncode = Label(app,text="Mensaje a ocultar", bg='#35D3A7', font=myFont)
lbl_txtEncode.place(x=475, y=82)
txtToEncode = Text(app, wrap=WORD, width=30)
txtToEncode.place(x=625, y=65, height=50)

lbl_keyEncode = Label(app,text="Clave para encriptar (mas corta)", bg='#35D3A7', font=myFont)
lbl_keyEncode.place(x=400, y=147)
keyToEncode = Text(app, wrap=WORD, width=30)
keyToEncode.place(x=625, y=130, height=50)

lbl_nameEncode = Label(app,text="Nombre (con extension)", bg='#35D3A7', font=myFont)
lbl_nameEncode.place(x=445, y=212)
nameEncode = Text(app, wrap=WORD, width=30)
nameEncode.place(x=625, y=195, height=50)

encrypt_btn = Button(app, text="Encode", bg='#8D41D6', fg='white', relief=RAISED, bd=3, pady= 3, padx = 3, font=myFont, command= lambda: encrypt_data_into_image(txtToEncode, keyToEncode, nameEncode))
encrypt_btn.place(x=718, y=260)

app.mainloop()
