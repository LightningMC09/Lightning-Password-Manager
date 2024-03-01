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
    
    # Code to take the characters in the list and make a password, then display it
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

    # If the user selects yes, delete the key and password files.
    if confirm:
        key_path = Path(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\a2V5cw\\{password_name.strip("=")}')
        pass_path = Path(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_name)}')
        key_path.unlink(missing_ok=True)
        pass_path.unlink(missing_ok=True)

        clearReadPassword() # Run clearReadPassword to hide all elements related to that password

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

    # Save Password to file
    pass_path = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\cGFzc3dvcmRz\\{b64d(password_name)}'
    os.makedirs(os.path.dirname(pass_path), exist_ok=True)
    with open(pass_path, 'wb') as password_file:  
        password_file.write(password_encrypted)

    # Show a message box to tell the user it worked
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

# copyPassword but for a read password
def copyReadPassword():
    password = read_password_label.get()
    pyperclip.copy(password)  

# Define the dark_mode variable, and set it to 1 if dark.mode contains 1 (Which gets set the user changes to dark mode)
def checkDarkMode():
    global dark_mode
    dark_mode = tk.IntVar()
    dark_file = f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\dark.mode'
    if os.path.exists(dark_file):
        with open(dark_file,'r') as f: # Open the file to read it
            dark_mode.set(int(f.read())) # Set dark_mode to the contents of the file
    style.theme_use('equilux' if dark_mode.get() == 1 else 'arc') # Set the ttk theme based on dark_mode
    window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7') # Set the window background as well, as it not a ttk widget

# Round the value of slider_length, because ttk.scale doesnt support tick to intervak
def roundSlider(x):
    slider_length.set(round(float(x)))

# Open the settings window, currently only having a toggle for dark mode and an exit button
def openSettings():

    # Exit function to be run with settings_window_quit
    def kill():
        settings_window.destroy()
    
    # Function to check value of dark_mode and change theme and window colors appropriately
    def toggleDarkmode():
        style.theme_use('equilux' if dark_mode.get() == 1 else 'arc') # Set the ttk theme
        window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7') # Set the main window color
        settings_icon.configure(file=icons[2 if dark_mode.get() == 1 else 1]) # Change the icon of the settings butotn
        settings_window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7') # Set the settings window color
        settings_window.update()
        with open(f'{os.getenv("APPDATA")}\\TGlnaHRuaW5nTUMwOQ\\dark.mode','w') as f:
            f.write(str(dark_mode)) # Write value of dark_mode to file, so later runs will automatically change theme

    # Code to make the settings window
    settings_window = tk.Toplevel(window)
    settings_window.resizable(False, False)
    window_settings_icon = tk.PhotoImage(file=icons[1], master=settings_window) # Make the icon of the window, originally used module darkdetect to detect user's theme, but on windows dark mode doesnt apply to window titles
    settings_window.wm_iconphoto(False, window_settings_icon) # Set the icon of the window
    settings_window.geometry('250x150')
    settings_window_quit = ttk.Button(settings_window,command=kill,text='Ok') # Simple exit button
    settings_window.configure(background='#464646' if dark_mode.get() == 1 else '#F5F6F7') # Set the background color based on theme
    dark_mode_checkbox = ttk.Checkbutton(settings_window, text='Dark mode?', variable=dark_mode, onvalue=1, offvalue=0,command=toggleDarkmode) # Checkbutton to toggle themes

    dark_mode_checkbox.pack(pady=3)
    settings_window_quit.pack(side='bottom',pady=10)

# Define the main window and its variables.
window = tk.Tk()
window.iconbitmap(icons[0])
window.title('Lightning Password Manager')
window.resizable(False, False) # Prevent window resizing (Because im too lazy to make it look good)
window.geometry('648x400')
window.configure(background='#F5F6F7')
style = ttkthemes.ThemedStyle(window)
style.theme_use('arc') # Use light theme, this will be changed if dark_mode is 1
checkDarkMode() # Check dark_mode so theme will automatically change

# Code to generate the 9 frames
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

        # My code to define contents of each frame, using tkk widgets where possible
        if i == 0 and j == 0:
            
            # Length slider and display
            length_label = ttk.Label(master=frame, text='Length:')
            slider_length = tk.IntVar()
            slider_label = ttk.Label(master=frame,textvariable=slider_length)
            slider = ttk.Scale(master=frame, from_=8, to=32, orient=tk.HORIZONTAL,variable=slider_length,command=roundSlider,length=170)
            slider.set(12)

            length_label.pack(pady=6)
            slider_label.pack()
            slider.pack()

        elif i == 0 and j == 1:

            # Generate button and password display
            generate_button = ttk.Button(master=frame, text='Generate', command=generatePassword)
            password_label = ttk.Entry(master=frame, width=38) # Using ttk.Entry as tk.Text has no ttk equivalent and ttk.Label doesnt allow selecting of text

            generate_button.pack(padx=5, pady=14)
            password_label.pack()

        elif i == 0 and j == 2:

            # Checkboxes to disable cApiTaLs, numb3r5, and $pec!@l ch@racter$
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

            # Button and entry to read a saved password
            read_button = ttk.Button(master=frame, text='Find Password:', command=readPassword)
            read_name = ttk.Entry(master=frame, width=15)
            read_name.bind('<Return>', readPassword)

            read_button.pack()
            read_name.pack(padx=3, pady=3)

        elif i == 1 and j == 1:

            # Display the read password and allow to copy it or delete (As well as clear from clipboar)
            read_password_label = ttk.Entry(master=frame, width=38) # Using ttk.Entry as tk.Text has no ttk equivalent and ttk.Label doesnt allow selecting of text
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

            # Save password button and name entry
            save_button = ttk.Button(master=frame, text='Save Password:', command=savePassword)
            save_name = ttk.Entry(master=frame, width=15)
            save_name.bind('<Return>', savePassword) # Using .bind() so the read password code will run when the user presses enterw

            save_button.pack_forget()
            save_name.pack_forget()

        elif i == 2 and j == 1:
            # Copy and clear buttons for generated password
            copy_button = ttk.Button(master=frame, text='Copy', command=copyPassword)
            clear_button = ttk.Button(master=frame, text='Clear', command=clearPassword)

            clear_button.pack_forget()
            copy_button.pack_forget()

# Start the gui
window.mainloop()
