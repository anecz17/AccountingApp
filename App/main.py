from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import datetime

import json
import tkinter as tk
from tkinter import *
from tkinter import simpledialog, messagebox  
from functools import partial
import pandas as pd
import os
import shutil


from ligetCafe.cafe import *
from ligetHotel.hotel import *
from adószámlázó.adoszamla import *
from előleg.előleg import *


with open("data.json", "r") as infile:
    felhasználónevek = json.load(infile)
    
bejelentkezési_adatok = []
global művelet
művelet = 0
global ado_window

def add_option():
    window.title("Hozzáadás")

    try:
        újcég = simpledialog.askstring("Input", "Adja meg az hozzáadandó cég nevét:")
        újfelh = simpledialog.askstring("Input", "Adja meg az hozzáadandó cég felhasználónevét:")
        felhasználónevek[újcég] = újfelh
        
        # Save the dictionary to a JSON file
        with open("data.json", "w") as outfile:
            json.dump(felhasználónevek, outfile)
    except:
        messagebox.showinfo("Alert", "A cégnév már foglalt! Válasszon másik nevet!")
    # Refresh the window
    refresh_window()

def delete_option():
    window.title("Törlés")
    # Clear existing buttons
    for widget in window.winfo_children():
        widget.destroy()
    
    # Create new buttons based on dictionary keys
    for cég in felhasználónevek:
        cég_button = tk.Button(window, text=cég, command=lambda c=cég: törlés(c))
        cég_button.pack()
        
    back_button = tk.Button(window, text="Vissza", command=back)
    back_button.pack()

def törlés(cég_to_delete):
    
    if cég_to_delete in felhasználónevek:
        del felhasználónevek[cég_to_delete]
        with open("data.json", "w") as outfile:
            json.dump(felhasználónevek, outfile)
        delete_option()  # Refresh the buttons
    else:
        messagebox.showerror("Error", "A megadott cég nem található.")
        
def back():
    #clear_window()
    refresh_window()
    
def refresh_window():
    adoszamlaIndito()
    
   
def ask_password(prompt):
    # Create a new top-level window for password input
    dialog = tk.Toplevel()
    dialog.title(prompt)
    
    # Create a label and an entry widget (with masking)
    tk.Label(dialog, text=prompt).pack(padx=20, pady=10)
    password_var = tk.StringVar()
    password_entry = tk.Entry(dialog, textvariable=password_var, show="*")  # show="*" masks the input
    password_entry.pack(padx=20, pady=10)
    
    # Create a button to submit the password
    def submit_password():
        dialog.quit()  # Close the window
        dialog.destroy()  # Destroy the window

    submit_button = tk.Button(dialog, text="Submit", command=submit_password)
    submit_button.pack(padx=20, pady=10)

    dialog.mainloop()  # Start the window loop

    # Return the entered password
    return password_var.get()

    
def választott(cég):
    print(f"User selected: {cég}")
    bejelentkezési_adatok.append(felhasználónevek[cég])
    #bejelentkezési_adatok.append(simpledialog.askstring("Input", "Adja meg a(z) " + cég + " felhasználónévhez tartozó jelszavát:", ))
    bejelentkezési_adatok.append(ask_password(f"Adja meg a(z) {cég} felhasználónévhez tartozó jelszavát:"))
    window.destroy()
    
   
def adoszamlaIndito():
    #window = tk.Tk()  # Create a new top-level window
    window.title("Választás")
    
    for widget in window.winfo_children():
        widget.destroy()
    
    for cég in list(felhasználónevek.keys()):
        cég_button = tk.Button(window, text=cég, command=lambda c=cég: választott(c))
        cég_button.pack()

    add_button = tk.Button(window, text="Hozzáadás", command=add_option)
    delete_button = tk.Button(window, text="Törlés", command=delete_option)
    
    add_button.pack()
    delete_button.pack()
    
    #window.destroy()
    
    

def utvonalModositas():
    útvonal = simpledialog.askstring("Input", "Fájlok helye:", initialvalue="D:\\elérési\\útvonal\\")
    refresh_window()
    
def ligetIndito():
    global művelet
    művelet = 1
    global útvonal
    
    with open("path.json", "r") as infile2:
        útvonal = json.load(infile2)
        print(útvonal)
        tmp = simpledialog.askstring("Input", "Fájlok helye:", initialvalue=útvonal)
    
    if útvonal != tmp:
        with open("path.json", "w") as outfile:
            json.dump(tmp, outfile)
        útvonal = tmp
        
    window.destroy()
    
def cafeIndito():
    global művelet
    művelet = 2
    global útvonal
    
    with open("path.json", "r") as infile2:
        útvonal = json.load(infile2)
        print(útvonal)
        tmp = simpledialog.askstring("Input", "Fájlok helye:", initialvalue=útvonal)
    
    if útvonal != tmp:
        with open("path.json", "w") as outfile:
            json.dump(tmp, outfile)
        útvonal = tmp
        
    window.destroy()
    
def előlegIndító():
    global művelet
    művelet = 3
    global útvonal
    
    with open("path.json", "r") as infile2:
        útvonal = json.load(infile2)
        print(útvonal)
        tmp = simpledialog.askstring("Input", "Fájlok helye:", initialvalue=útvonal)
    
    if útvonal != tmp:
        with open("path.json", "w") as outfile:
            json.dump(tmp, outfile)
        útvonal = tmp
        
    window.destroy()

def menu():
    window.title("Tevékenység")
    
    adoszamlaLekerdezes = tk.Button(window, text="Adószámla Lekérdezés", command=adoszamlaIndito)
    ligetMakro = tk.Button(window, text="Liget Hotel", command=ligetIndito)
    cafeMakro = tk.Button(window, text="Liget Cafe", command=cafeIndito)
    előleg = tk.Button(window, text="Párosítás", command=előlegIndító)
    
    adoszamlaLekerdezes.pack()
    ligetMakro.pack()
    cafeMakro.pack()
    előleg.pack()

    
    
### main() ###
# Create the main window
window = tk.Tk()
window.title("Tevékenység")

menu()

# Start the main event loop
window.mainloop()

if művelet == 0:
    adószámlázó()
    
elif művelet == 1:
    ligetHotel(útvonal=útvonal)
    
elif művelet == 2:
    ligetCafe(útvonal=útvonal)
    
elif művelet == 3:
    előleg(útvonal=útvonal)
    
    
        