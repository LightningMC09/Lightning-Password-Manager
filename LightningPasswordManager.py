from random import choices
from cryptography.fernet import Fernet
from pathlib import Path
from requests import get
import ttkthemes
import pyperclip
import os
import base64
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

# Functions to encode and decode b64
def b64e(s): 
    return base64.b64encode(s.encode()).decode()

def b64d(s): 
    return base64.b64decode(s).decode()

# Code to download icon files from github as needed
icons_directory = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\YXNzZXRz\\'

icons = ['icon.ico', 'settings_light.png', 'settings_dark.png' ]
icons[:] = [icons_directory + s for s in icons] # Prepending icons_directory to every item in icons

# List of urls to download
urls = ['https://raw.githubusercontent.com/lightnignmc09/Lightning-Password-Manager/main/Assets/icon.ico',
       'https://raw.githubusercontent.com/lightnignmc09/Lightning-Password-Manager/main/Assets/settings_light.png',
       'https://raw.githubusercontent.com/lightnignmc09/Lightning-Password-Manager/main/Assets/settings_dark.png']
os.makedirs(os.path.dirname(icons[0]), exist_ok=True) # Make path to save icons to if it doesnt exist

# If it does exist, check that the local 'icon.ico' is different than the github file
if os.path.exists(icons[0]):
    r = get(urls[0]) # Request github file
    with open(icons[0],'rb') as f:
        if not f.read() == (r.content): # Check if they are different
            # Go through list of urls and write content to file (Essentialy download the files)
            for i, url in enumerate(urls):
                r = get(url)
                with open(icons[i], 'wb') as f:
                    f.write(r.content)
else:
    # if it doesnt exist, go through list of urls and write content to file (Essentialy download the files)
    for i, url in enumerate(urls):
        r = get(url)
        with open(icons[i], 'wb') as f:
            f.write(r.content)

# Code to actually generate the password, based on the values of capitals, numbers, and specials
def generatePassword():
    characters = list('abcdefghijklmnopqrstuvwxyz')
    password_length = int(slider.get())
    # Extending the list with more characters based on users choices
    if capitals.get():
        characters.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if numbers.get():
        characters.extend('0123456789')
    if specials.get():
        characters.extend('!@#$%^&*')
    
    password = "".join(choices(characters, k=password_length))
    password_label.delete(0, tk.END)
    password_label.insert(0, password)
    copy_button.pack(side='left', anchor='nw')
    clear_button.pack(padx=3, side='left', anchor='ne')
    save_name.pack(pady=3, side='bottom')
    save_button.pack(side='bottom')

# Copy password from password_label to clipboard
def copyPassword():
    password = password_label.get()
    pyperclip.copy(password)  

# Add blank value to clipboard, and hide clear, copy and save buttons.
def clearPassword():
    pyperclip.copy(' ')
    password_label.delete(1, tk.END)  
    clear_button.pack_forget()  
    copy_button.pack_forget()  
    save_button.pack_forget()
    save_name.pack_forget()

# Delete the currently read password, after asking for confirmation
def deleteReadPassword():
    password_name = b64e(read_name.get().strip().lower()) # Using .strip() and .lower() so whitespace at the beggining and end will be removed, and so it wont be case sensitive
    confirm = tkMessageBox.askyesno(title='Confirmation', message=f'Are you sure you want to delete {b64d(password_name)}?')
    if confirm:
        key_path = Path(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\a2V5cw\\{password_name.strip("=")}')
        pass_path = Path(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_name)}')
        key_path.unlink(missing_ok=True)
        pass_path.unlink(missing_ok=True)
        clearReadPassword()

# Encrypt password and save it and its key to a file, encoding the key's filename in base64
def savePassword(x=""):
    password = password_label.get()  
    password_name = b64e(save_name.get().strip().lower()) # Using .strip() and .lower() so whitespace at the beggining and end will be removed, and so it wont be case sensitive
    key = Fernet.generate_key() # Generate key

    # Save key to file
    key_path = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\a2V5cw\\{password_name.strip("=")}'
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    with open(key_path, 'wb') as filekey:
        filekey.write(key)
    
    # Encrypt password
    password_encrypted = Fernet(key).encrypt(password.encode())  
    pass_path = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_name)}'
    os.makedirs(os.path.dirname(pass_path), exist_ok=True)
    with open(pass_path, 'wb') as password_file:  
        password_file.write(password_encrypted)
    print('Password saved!')

    tkMessageBox.showinfo(title='Success', message='Password Saved Successfully!')

# Code to decrypt password depending on what the user typed, if it doesnt exist give them a messagebox
def readPassword(x=""):
    clearReadPassword()
    padding = 40
    password_read = b64e(read_name.get().strip().lower()) # Using .strip() and .lower() so whitespace at the beggining and end will be removed, and so it wont be case sensitive
    if os.path.exists(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_read)}'):
        pf = open(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_read)}', 'rb')
        read_password = pf.read()
        kf = open(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\a2V5cw\\{password_read.strip("=")}', 'rb')
        key = kf.read()
        decrypted_password = Fernet(key).decrypt(read_password).decode() # Decrypt the password based on a base64 encoding of what the user typed
        read_password_label.delete(0, tk.END)
        print(decrypted_password)
        read_password_label.insert(0, decrypted_password)
        read_password_label.pack()
        clear_read.pack(padx=(padding, 0), pady=3, side='left')
        delete_read.pack(padx=(0, padding), pady=3, side='right')
        copy_read.pack(pady=4,padx=3)
    else:
        tkMessageBox.showinfo(title='Error', message='Password not found! Check that you spelled it right and try again.')

# Clear add blank space to clipboard and hide read password, clear, copy, and delete buttons
def clearReadPassword():
    pyperclip.copy(' ')
    read_password_label.pack_forget()
    clear_read.pack_forget()
    copy_read.pack_forget()
    delete_read.pack_forget()

def copyReadPassword():
    password = read_password_label.get()
    pyperclip.copy(password)  

def checkDarkMode():
    global dark_mode
    dark_mode = tk.IntVar()
    with open(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\dark.mode','r') as f:
        dark_mode.set(1 if f.read() == '1' else 0)
    style.theme_use('equilux' if dark_mode.get() == 1 else 'arc')
    window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7')

def roundSlider(x):
    slider_length.set(round(float(x)))

def openSettings():

    def kill():
        settings_window.destroy()

    def toggleDarkmode():
        style.theme_use('equilux' if dark_mode.get() == 1 else 'arc')
        window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7')
        settings_icon.configure(file=icons[2 if dark_mode.get() == 1 else 1])
        settings_window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7')
        settings_window.update()
        with open(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\dark.mode','w') as f:
            f.write('1' if dark_mode.get() == 1 else '0')

    settings_window = tk.Toplevel(window)
    settings_window.resizable(False, False)
    window_settings_icon = tk.PhotoImage(file=icons[1], master=settings_window)
    settings_window.wm_iconphoto(False, window_settings_icon)
    settings_window.geometry('250x150')
    settings_window_quit = ttk.Button(settings_window,command=kill,text='Ok')
    settings_window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7')
    dark_mode_checkbox = ttk.Checkbutton(settings_window, text='Dark mode?', variable=dark_mode, onvalue=1, offvalue=0,command=toggleDarkmode)
    dark_mode_checkbox.pack(pady=3)
    settings_window_quit.pack(side='bottom',pady=10)

window = tk.Tk()
window.iconbitmap(icons[0])
window.title('Lightning Password Manager')
window.resizable(False, False)
window.geometry('648x400')
style = ttkthemes.ThemedStyle(window)
style.theme_use('arc')
window.configure(background='#F5F6F7')
checkDarkMode()

for i in range(3):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)
    for j in range(0, 3):
        frame = ttk.Frame(
            master=window,
            relief=tk.FLAT,
            border=False
        )

        frame.grid(row=i, column=j, padx=5, pady=5)
        if i == 0 and j == 0:
            length_label = ttk.Label(master=frame, text='Length:')
            slider_length = tk.IntVar()
            slider_label = ttk.Label(master=frame,textvariable=slider_length)
            slider = ttk.Scale(master=frame, from_=8, to=32, orient=tk.HORIZONTAL,variable=slider_length,command=roundSlider,length=170)
            slider.set(12)
            length_label.pack(pady=6)
            slider_label.pack()
            slider.pack()
        elif i == 0 and j == 1:
            generate_button = ttk.Button(master=frame, text='Generate', command=generatePassword)
            password_label = ttk.Entry(master=frame, width=38)
            generate_button.pack(padx=5, pady=14)
            password_label.pack()
        elif i == 0 and j == 2:
            capitals = tk.IntVar(value=1)
            numbers = tk.IntVar(value=1)
            specials = tk.IntVar(value=1)

            capitals_check = ttk.Checkbutton(master=frame, text='Capitals?', variable=capitals, onvalue=1, offvalue=0)
            numbers_check = ttk.Checkbutton(master=frame, text='Numbers?', variable=numbers, onvalue=1, offvalue=0)
            special_check = ttk.Checkbutton(master=frame, text='Specials?', variable=specials, onvalue=1, offvalue=0)

            capitals_check.pack()
            numbers_check.pack(pady=12)
            special_check.pack()
        elif i == 1 and j == 0:
            read_button = ttk.Button(master=frame, text='Find Password:', command=readPassword)
            read_name = ttk.Entry(master=frame, width=15)
            read_name.bind('<Return>', readPassword)
            read_button.pack()
            read_name.pack(padx=3, pady=3)
        elif i == 1 and j == 1:
            read_password_label = ttk.Entry(master=frame, width=38)
            clear_read = ttk.Button(master=frame, text='Clear', command=clearReadPassword)     
            copy_read = ttk.Button(master=frame, text='Copy', command=copyReadPassword)  
            delete_read = ttk.Button(master=frame, text='Delete', command=deleteReadPassword)
            read_password_label.pack_forget()
            clear_read.pack_forget()
            copy_read.pack_forget()
            delete_read.pack_forget()
        elif i == 1 and j == 2:
            settings_icon = tk.PhotoImage(master=frame, file=icons[2 if dark_mode.get() == 1 else 1])
            settings_button = ttk.Button(master=frame, image=settings_icon,width=35,command=openSettings)
            settings_button.pack()
        elif i == 2 and j == 0:
            save_button = ttk.Button(master=frame, text='Save Password:', command=savePassword)
            save_name = ttk.Entry(master=frame, width=15)
            save_name.bind('<Return>', savePassword)
            save_button.pack_forget()
            save_name.pack_forget()
        elif i == 2 and j == 1:
            copy_button = ttk.Button(master=frame, text='Copy', command=copyPassword)
            clear_button = ttk.Button(master=frame, text='Clear', command=clearPassword)
            clear_button.pack_forget()
            copy_button.pack_forget()
print('App launched successfully!')
window.mainloop()
