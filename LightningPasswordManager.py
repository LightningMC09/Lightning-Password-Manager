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

# Base64 encoding and decoding functions
def b64e(s):
    return base64.b64encode(s.encode()).decode()

def b64d(s):
    return base64.b64decode(s).decode()

# Download the icon files from GitHub (thanks GitHub!)
icons_directory = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\YXNzZXRz\\'

icon1_filename = icons_directory + 'icon.ico'
icon2_filename = icons_directory + 'settings.png'
os.makedirs(os.path.dirname(icon1_filename), exist_ok=True)
if os.path.exists(icon1_filename) or os.path.exists(icon2_filename):
    os.unlink(icon1_filename)
    os.unlink(icon2_filename)
url = 'https://raw.githubusercontent.com/lightnignmc09/Lightning-Password-Manager/main/Assets/icon.ico'
r = get(url)
with open(icon1_filename, 'wb') as f:
    f.write(r.content)
url = 'https://raw.githubusercontent.com/lightnignmc09/Lightning-Password-Manager/main/Assets/settings.png'
r = get(url)
with open(icon2_filename, 'wb') as f:
    f.write(r.content)

# Function to generate a random password based on user preferences
def generatePassword():
    characters = list('abcdefghijklmnopqrstuvwxyz')
    password_length = int(slider.get())
    if capitals.get():
        characters.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if numbers.get():
        characters.extend('0123456789')
    if specials.get():
        characters.extend('!@#$%^&*')
    password = "".join(choices(characters, k=64))[:password_length]
    password_label.delete(0, tk.END)
    password_label.insert(0, password)

    # Make copy button visible after generating a password
    copy_button.pack(side='left', anchor='nw')
    clear_button.pack(padx=3, side='left', anchor='ne')
    save_name.pack(pady=3, side='bottom')
    save_button.pack(side='bottom')

# Function to copy the generated password to the clipboard
def copyPassword():
    password = password_label.get()
    pyperclip.copy(password)  # Copy password to clipboard

# Function to clear the generated password and buttons
def clearPassword():
    password_label.configure(state='normal')
    password_label.delete(1, tk.END)  # Clear password label
    clear_button.pack_forget()  # Hide clear button
    copy_button.pack_forget()  # Hide copy button
    save_button.pack_forget()
    save_name.pack_forget()
    password_label.configure()
    pyperclip.copy(' ')

# Function to delete a saved password
def deleteReadPassword():
    password_name = b64e(read_name.get().strip().lower())
    confirm = tkMessageBox.askyesno(title='Confirmation', message=f'Are you sure you want to delete {b64d(password_name)}?')
    if confirm:
        key_path = Path(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\a2V5cw\\{password_name.strip("=")}')
        pass_path = Path(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_name)}')
        key_path.unlink(missing_ok=True)
        pass_path.unlink(missing_ok=True)
        clearReadPassword()

# Function to save the generated password as an encrypted file
def savePassword(x=""):
    password = password_label.get()  # Get the password to encrypt and save
    password_name = b64e(save_name.get().strip().lower())  # Get the name to save it as (e.g., youtube)
    key = Fernet.generate_key()  # Generate key
    key_path = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\a2V5cw\\{password_name.strip("=")}'
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    with open(key_path, 'wb') as filekey:  # Write key
        filekey.write(key)
    password_encrypted = Fernet(key).encrypt(password.encode())  # Encode password
    pass_path = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_name)}'
    os.makedirs(os.path.dirname(pass_path), exist_ok=True)
    with open(pass_path, 'wb') as password_file:  # Write encrypted password
        password_file.write(password_encrypted)
    print('Password saved!')

    tkMessageBox.showinfo(title='Success', message='Password Saved Successfully!')

# Function to read a saved password from an encrypted file
def readPassword(x=""):
    clearReadPassword()
    padding = 40
    password_read = b64e(read_name.get().strip().lower())
    if os.path.exists(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_read)}'):
        pf = open(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_read)}', 'rb')
        read_password = pf.read()
        kf = open(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\a2V5cw\\{password_read.strip("=")}', 'rb')
        key = kf.read()
        decrypted_password = Fernet(key).decrypt(read_password).decode()
        read_password_label.pack()
        read_password_label.delete(0, tk.END)
        print(decrypted_password)
        read_password_label.insert(0, decrypted_password)
        clear_read.pack(padx=(padding, 0), pady=3, side='left')
        delete_read.pack(padx=(0, padding), pady=3, side='right')
        copy_read.pack(pady=4,padx=3)
    else:
        tkMessageBox.showinfo(title='Error', message='Password not found! Check that you spelled it right and try again.')

# Function to clear the read password and buttons
def clearReadPassword():
    read_password_label.pack_forget()
    clear_read.pack_forget()
    copy_read.pack_forget()
    delete_read.pack_forget()
    pyperclip.copy(' ')

# Function to copy the read password to the clipboard
def copyReadPassword():
    password = read_password_label.get()
    pyperclip.copy(password)  # Copy password to clipboard

# Function to open settings menu
def openSettings():
    global dark_mode
    dark_mode = tk.IntVar()
    if dark_mode is None:
        dark_mode = tk.IntVar(value=0)
    
    def toggleDarkMode():
        style.theme_use('equilux' if dark_mode.get() == 1 else 'arc')
        window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7')
        settings_window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7')
        settings_window.update()

    settings_window = tk.Toplevel(window)
    settings_window.resizable(False, False)
    alt_settings_icon = tk.PhotoImage(file=icon2_filename, master=settings_window)
    settings_window.wm_iconphoto(False, alt_settings_icon)
    settings_window.geometry('250x150')
    settings_window.configure(background='#F5F6F7')
    dark_mode_checkbox = ttk.Checkbutton(settings_window, text='Dark mode?', variable=dark_mode, onvalue=1, offvalue=0,command=toggleDarkMode)
    dark_mode_checkbox.pack()
# Create the main window
window = tk.Tk()
window.iconbitmap(icon1_filename)
window.title('Lightning Password Manager')
window.resizable(False, False)
window.geometry('607x214')
style = ttkthemes.ThemedStyle(window)
style.theme_use('arc')
window.configure(background='#F5F6F7')

# tell tcl where to find the awthemes packages

# Set up the window grid
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
            # Password length label and entry
            length_label = ttk.Label(master=frame, text='Length:')
            length_label.pack(pady=6)
            # Slider for password length
            slider = ttk.Scale(master=frame, from_=8, to=32, orient=tk.HORIZONTAL)
            slider.set(12)
            slider.pack()
        elif i == 0 and j == 1:
            # Generate button
            generate_button = ttk.Button(master=frame, text='Generate', command=generatePassword)
            generate_button.pack(padx=5, pady=14)
            # Password label
            password_label = ttk.Entry(master=frame, width=48)
            password_label.pack()
        elif i == 0 and j == 2:
            # Checkboxes to include/exclude characters in generated password
            capitals = tk.IntVar(value=1)
            numbers = tk.IntVar(value=1)
            specials = tk.IntVar(value=1)

            capitals_check = ttk.Checkbutton(master=frame, text='Capitals?', variable=capitals, onvalue=1, offvalue=0)
            capitals_check.pack()
            numbers_check = ttk.Checkbutton(master=frame, text='Numbers?', variable=numbers, onvalue=1, offvalue=0)
            numbers_check.pack(padx=1)
            special_check = ttk.Checkbutton(master=frame, text='Specials?', variable=specials, onvalue=1, offvalue=0)
            special_check.pack()
        elif i == 1 and j == 0:
            # Entry and button to find and display a saved password
            frame.configure(borderwidth=0)
            read_button = ttk.Button(master=frame, text='Find Password:', command=readPassword)
            read_button.pack()
            read_name = ttk.Entry(master=frame, width=15)
            read_name.bind('<Return>', readPassword)
            read_name.pack(padx=3, pady=3)
        elif i == 1 and j == 1:
            # Text widget to display a found password
            read_password_label = ttk.Entry(master=frame, width=48)
            read_password_label.pack_forget()
            frame.configure(borderwidth=0)
            clear_read = ttk.Button(master=frame, text='Clear Password', command=clearReadPassword)
            clear_read.pack_forget()
            copy_read = ttk.Button(master=frame, text='Copy to Clipboard', command=copyReadPassword)
            copy_read.pack_forget()
             # Button to delete a saved password
            delete_read = ttk.Button(master=frame, text='Delete Password', command=deleteReadPassword)
            delete_read.pack_forget()
            frame.configure(borderwidth=0)
        elif i == 1 and j == 2:
            settings_icon = tk.PhotoImage(master=frame, file=icon2_filename)
            settings_button = ttk.Button(master=frame, image=settings_icon,width=35,command=openSettings)
            settings_button.pack()
            frame.configure(borderwidth=0)
        elif i == 2 and j == 0:
            # Entry and button to save a generated password
            frame.configure(borderwidth=0)
            save_button = ttk.Button(master=frame, text='Save Password:', command=savePassword)
            save_button.pack_forget()
            save_name = ttk.Entry(master=frame, width=15)
            save_name.bind('<Return>', savePassword)
            save_name.pack_forget()
        elif i == 2 and j == 1:
            # Button to copy a generated password to clipboard
            frame.configure(borderwidth=0)
            copy_button = ttk.Button(master=frame, text='Copy to Clipboard', command=copyPassword)
            copy_button.pack_forget()
            # Button to clear a generated password
            clear_button = ttk.Button(master=frame, text='Clear Password', command=clearPassword)
            clear_button.pack_forget()

print('App launched successfully!')
window.mainloop()
