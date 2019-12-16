try:
    import os
    from tkinter import *
    
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog

from crypto import *
from crypto.cipher import *
import os
import os.path
from os import listdir
from os.path import isfile, join
import time

root = Tk()
root.title("Lock All Lock")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#==============================VARIABLES======================================
REPASSWORD = StringVar()
PASSWORD = StringVar()

#==============================FRAMES=========================================
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)

#==============================LABELS=========================================
lbl_title = Label(Top, text = "Lock All Lock", font=('arial', 15))
lbl_title.pack(fill=X)

if os.path.isfile('data.txt.enc'):
    lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
    lbl_password.grid(row=0, sticky="e")
    password = Entry(Form, textvariable=PASSWORD, font=(14))
    password.grid(row=0, column=1)

    
else:
    lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
    lbl_password.grid(row=0, sticky="e")
    lbl_repassword = Label(Form, text = "Re-Password:", font=('arial', 14), bd=15)
    lbl_repassword.grid(row=1, sticky="e")
    lbl_text = Label(Form)
    lbl_text.grid(row=2, columnspan=2)

    password = Entry(Form, textvariable=PASSWORD, font=(14))
    password.grid(row=0, column=1)
    repassword = Entry(Form, textvariable=REPASSWORD, show="*", font=(14))
    repassword.grid(row=1, column=1)
    

def log_in():
    if os.path.isfile('data.txt.enc'):
        while True:
            password = PASSWORD.get()
            enc.decrypt_file("data.txt.enc")
            p = ''
            with open("data.txt", "r") as f:
                p = f.readlines()
            if p[0] == password:
                enc.encrypt_file("data.txt")
                break


    else:
        while True:                    
            password = PASSWORD.get()
            repassword = REPASSWORD.get()
            if password == repassword:
                break
            else:
                lbl_text.configure(text = "Passwords Mismatched!")
        f = open("data.txt", "w+")
        f.write(password)
        f.close()
        enc.encrypt_file("data.txt")
        lbl_text.configure(text = "Please restart the program to complete the setup")
        time.sleep(15)
		

 
#==============================BUTTON WIDGETS=================================
login_btn = Button(Form, text="Log in!", command = log_in, bg="#93ff00")
login_btn.bind('<Return>', log_in)
login_btn.grid(row=5, column=5, sticky='NESW')

root.mainloop()



class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'LockAllLock.py' and fname != 'data.txt.enc'):
                    dirs.append(dirName + "//" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = encrypt_file_open()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = decrypt_file_open()
        for file_name in dirs:
            self.decrypt_file(file_name)



    

def encrypt_file_open():
    rep = filedialog.askopenfilenames(
    	parent=root,
    	initialdir='/',
    	initialfile='',
    	filetypes=[
    		("All files", "*")])
    
    try:
	    return (rep)
    except IndexError:
        print("No file selected")

def decrypt_file_open():
    rep = filedialog.askopenfilenames(
    	parent=root,
    	initialdir='/',
    	initialfile='',
    	filetypes=[
    		(".enc", "*.enc")])
    
    try:
	    return (rep)
    except IndexError:
        print("No file selected")




key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
clear = lambda: os.system('clear')

