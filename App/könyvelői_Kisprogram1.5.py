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

def menu():
    window.title("Tevékenység")
    
    adoszamlaLekerdezes = tk.Button(window, text="Adószámla Lekérdezés", command=adoszamlaIndito)
    ligetMakro = tk.Button(window, text="Liget Hotel", command=ligetIndito)
    cafeMakro = tk.Button(window, text="Liget Cafe", command=cafeIndito)
    
    adoszamlaLekerdezes.pack()
    ligetMakro.pack()
    cafeMakro.pack()
    
    
    
def adószámlázó():
    # Initialize the Firefox WebDriver
    driver = webdriver.Firefox()

    # Open the website
    website_url = "https://ebev.nav.gov.hu/"
    driver.get(website_url)

    # Bejelentkezés KAÜvel katt
    button_id = "loginBtn"
    button_element = driver.find_element("id", button_id)
    button_element.click()

    # Ügyfélkapu katt
    time.sleep(2.5)
    form_id = "urn:eksz.gov.hu:1.0:azonositas:kau:1:uk:uidpwd"
    form_element = driver.find_element("id", form_id)
    form_element.submit()

    """tabindex_value = "0"  # Replace with the desired tabindex value
    element_to_click = driver.find_element(By.CSS_SELECTOR, f'[tabindex="{tabindex_value}"]')
    element_to_click.click()"""


    #kérj bejelentkezési adatokat
    time.sleep(7)

    # Bejelentkezési Adatok
    input_id = "fldUser"
    input_element = driver.find_element("id", input_id)
    input_element.send_keys(bejelentkezési_adatok[0])

    #jelszó = "Andristeszt2023"
    input_id = "fldPass"
    input_element = driver.find_element("id", input_id)
    input_element.send_keys(bejelentkezési_adatok[1])

    # Bejelentkezés katt
    button_class = "button.btn.btn-blue.btn-block.btn-md.center-block"
    button_element = driver.find_element("css selector", button_class)
    button_element.click()
    time.sleep(8)

    # Adószámlához átjutni
    body = driver.find_element("tag name", "body")
    time.sleep(0.5)
    body.click()
    tabindex_value = "-1"  # Replace with the desired tabindex value
    element_to_click = driver.find_element(By.CSS_SELECTOR, f'[tabindex="{tabindex_value}"]')
    element_to_click.click()
    actions = ActionChains(driver)
    actions.move_to_element(body)
    actions.perform()
    for _ in range(4):
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.2)
    body.send_keys(Keys.ARROW_RIGHT)
    body.send_keys(Keys.ENTER)
    time.sleep(1)

    #Ellenőrzi, hogy átjutott-e az adószámlához
    while(1):
        cím = driver.find_element("id", "main_content")
        # Rossz oldal
        if cím.text != "Adószámla":
            driver.refresh()
            time.sleep(0.5)
            body = driver.find_element("tag name", "body")
            body.click()
            tabindex_value = "-1" 
            element_to_click = driver.find_element(By.CSS_SELECTOR, f'[tabindex="{tabindex_value}"]')
            element_to_click.click()
            actions = ActionChains(driver)
            actions.move_to_element(body)
            actions.perform()
            for _ in range(4):
                body.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
            body.send_keys(Keys.ARROW_RIGHT)
            body.send_keys(Keys.ENTER)
            time.sleep(0.1)
            
            body.send_keys(Keys.TAB)        
            body.send_keys(Keys.TAB)
            body.send_keys(Keys.ENTER)
            time.sleep(1)
            continue
                
        button_id = "igenyNavGomb"
        button_element = driver.find_element("id", button_id)
        button_element.click()
        break
            
        

    time.sleep(1)

    # Mai nap
    current_datetime = datetime.datetime.now()
    print("Current Date and Time:", current_datetime)

    # Extract individual components
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day

    if current_day < 28:
        if current_month < 10:
            current_month = '0' + str(current_month)
        időszak = str(current_year) + '.' + str(current_month) + '.28'
    else:
        if current_month == 12:
            current_year += 1
            időszak = str(current_year) + '.01.28'
        else:
            current_month += 1
            if current_month < 10:
                current_month = '0' + str(current_month)
            időszak = str(current_year) + '.' + str(current_month) + '.28'



    # Ügyfelek adatainak lekérdezése
    # Locate the input element
    input_element = driver.find_element("name", "0")

    if input_element.is_displayed():
        print("Több ügyfél van")
        select_element = driver.find_element("id", "0")
        select = Select(select_element)
        ügyfelek = len(select.options)
    else:
        print("1 ügyfél van")
        ügyfelek = 1
        

    #Törlés, ha kell
    li_element = driver.find_element("css selector", ".navigatorIndex")
    li_text = li_element.text

    # Split the text to extract the values
    values = li_text.split(' / ')
    current_page = li_text.split('/')[0].strip() 
    if int(current_page) != 0:
        total_pages = li_text.split('/')[1].split('(')[0].strip()
        total_items = li_text.split('(')[1].split(')')[0].strip()

        print("Current Page:", current_page)
        print("Total Pages:", total_pages)
        print("Total Items:", total_items)

        # Oldalanként töröl
        for i in range(int(total_pages)):
            element = driver.find_element("xpath", "//img[@alt='Utolsó oldal']")
            element.click()

            time.sleep(0.5)
            checkbox = driver.find_element("xpath", "//input[@title='Az összes kijelölése az oldalon.']")
            checkbox.click()
            
            button = driver.find_element("xpath", "//input[@title='A kijelölt tételek törlése.']")
            button.click()
            
            alert = driver.switch_to.alert
            alert.accept()
            
            time.sleep(1)
            
            
    # Lekérdezések
    if ügyfelek == 1:
        button_id = "igenyLekIndit"
        button_element = driver.find_element("id", button_id)
        button_element.click()
    else:
        for i in range(ügyfelek):
            # Időszak megadása
            element = driver.find_element("id", "65")
            element.clear()
            element.send_keys(időszak)
            select_element = driver.find_element("id", "0")
            select = Select(select_element) 
            options = select.options
            
            option_text = options[i].text
            print("Selecting option:", option_text)
            select.select_by_visible_text(option_text)


            button_id = "igenyLekIndit"
            button_element = driver.find_element("id", button_id)
            button_element.click()
        

    # Letöltés
    # Ha több, mint 10
    if ügyfelek > 10:
        time.sleep(50)
        element = driver.find_element("xpath", "//img[@alt='Utolsó oldal']")
        element.click()
        
        checkbox = driver.find_element("xpath", "//input[@title='Az összes kijelölése az oldalon.']")
        checkbox.click()
        
        button = driver.find_element("xpath", "//input[@title='A kijelölt tételek tömörített letöltése.']")
        button.click()
        
        ügyfelek -= 10
        
        while ügyfelek>0:
            time.sleep(15)
            
            checkbox = driver.find_element("xpath", "//input[@title='Az összes kijelölése az oldalon.']")
            checkbox.click()
            
            element = driver.find_element("xpath", "//img[@alt='Előző oldal']")
            element.click()
            
            checkbox = driver.find_element("xpath", "//input[@title='Az összes kijelölése az oldalon.']")
            checkbox.click()
            
            button = driver.find_element("xpath", "//input[@title='A kijelölt tételek tömörített letöltése.']")
            button.click()
            
            ügyfelek -= 10

    # Ha kevesebb
    else:
        time.sleep(60)
        element = driver.find_element("xpath", "//img[@alt='Előző oldal']")
        element.click()
        
        checkbox = driver.find_element("xpath", "//input[@title='Az összes kijelölése az oldalon.']")
        checkbox.click()
        
        button = driver.find_element("xpath", "//input[@title='A kijelölt tételek tömörített letöltése.']")
        button.click()

    # Böngésző bezárása
    # driver.quit()
    


def hotelezőMakró(df):
    
    # To prevent dtype error
    df["Tétel árbevétel főkönyv"] = None
    df["Tétel árbevétel áfa"] = None
    df["Tétel gazdasági esemény"] = None
    df["Tétel áfa gazdasági esemény"] = None
    
    # Iterate through every row
    for index, row in df.iterrows():
        vevo_adoszam = row['Vevő adószám']

        #Adószám oszlop
        if pd.isna(vevo_adoszam):
            #print(f"NaN value found in row {index + 1}")
            df.at[index, "Vevő neve"] = "Magánszemély vevő"
            df.at[index, "Vevő irsz."] = None
            df.at[index, "Vevő város"] = None
            df.at[index, "Vevő utca"] = None
            # Add your actions for NaN values in each row
        #else:
            #print(f"Non-NaN value found in row {index + 1}: {vevo_adoszam}")
            # Add your actions for non-NaN values in each row
        
        
         
        #Áfakulcs oszlop
        if row["Áfakulcs"] == "ATK":
            df.at[index, "Tétel áfa gazdasági esemény"] = "ATHK"     
        else:
            df.at[index, "Tétel árbevétel áfa"] = "4671"
            if row["Áfakulcs"] == "27":
                df.at[index, "Tétel áfa gazdasági esemény"] = "27%"
            elif row["Áfakulcs"] == "5":
                substring = 'Előleg'
                if substring.lower() in row['Termék,szolgáltatás'].lower():
                    df.at[index, "Tétel áfa gazdasági esemény"] = "ELO5"
                else:
                    df.at[index, "Tétel áfa gazdasági esemény"] = "5%"
            
        #Termék,szolgáltatás --> Tétel árbevétel főkönyv, Tétel gazdasági esemény
        ifa = ["ifa", "idegenforgalmi adó"]
        szervizdij = ["szervízdíj", "szervizdíj", "szervízdij", "szervizdij"]
        if "előleg" in row['Termék,szolgáltatás'].lower() or "egycélú" in row['Termék,szolgáltatás'].lower():
            df.at[index, "Tétel árbevétel főkönyv"] = "4531"
        elif "szállás" in row['Termék,szolgáltatás'].lower():
            df.at[index, "Tétel árbevétel főkönyv"] = "9111"
            df.at[index, "Tétel gazdasági esemény"] = "!11"
        #szervízdíj
        elif szervizdij[0] in row['Termék,szolgáltatás'].lower() or szervizdij[1] in row['Termék,szolgáltatás'].lower() or szervizdij[2] in row['Termék,szolgáltatás'].lower() or szervizdij[3] in row['Termék,szolgáltatás'].lower():
            df.at[index, "Tétel árbevétel főkönyv"] = "9123"
            if row["Áfakulcs"] == "27":
                df.at[index, "Tétel gazdasági esemény"] = "!32"
            if row["Áfakulcs"] == "5":
                df.at[index, "Tétel gazdasági esemény"] = "!31"
        elif "étel" in row['Termék,szolgáltatás'].lower() or \
                "félpanzió" in row['Termék,szolgáltatás'].lower() or \
                "étkezés" in row['Termék,szolgáltatás'].lower() or \
                "reggeli" in row['Termék,szolgáltatás'].lower() or \
                "ebéd" in row['Termék,szolgáltatás'].lower() or \
                "vacsora" in row['Termék,szolgáltatás'].lower() or \
                ("kedvezmény" in row['Termék,szolgáltatás'].lower() and "5" in row['Termék,szolgáltatás'].lower()):
            df.at[index, "Tétel árbevétel főkönyv"] = "9121"
            df.at[index, "Tétel gazdasági esemény"] = "!31"
        elif "vital" in row['Termék,szolgáltatás'].lower() and "masszázs" in row['Termék,szolgáltatás'].lower(): 
            df.at[index, "Tétel árbevétel főkönyv"] = "9114"
            df.at[index, "Tétel gazdasági esemény"] = "!21"
        elif "ital" in row['Termék,szolgáltatás'].lower() or \
                "pepsi" in row['Termék,szolgáltatás'].lower() or \
                "liget víz" in row['Termék,szolgáltatás'].lower() or \
                "limonádé" in row['Termék,szolgáltatás'].lower() or \
                "toma prémium" in row['Termék,szolgáltatás'].lower() or \
                "szent andrás" in row['Termék,szolgáltatás'].lower() or \
                "szódavíz" in row['Termék,szolgáltatás'].lower() or \
                "pohár" in row['Termék,szolgáltatás'].lower() or \
                "cappuccino" in row['Termék,szolgáltatás'].lower() or \
                "jeges kávé" in row['Termék,szolgáltatás'].lower() or \
                "espresso" in row['Termék,szolgáltatás'].lower() or \
                "hosszúlépés" in row['Termék,szolgáltatás'].lower() or \
                "nagyfröccs" in row['Termék,szolgáltatás'].lower() or \
                "szentkirályi szénsav" in row['Termék,szolgáltatás'].lower() or \
                "schweppes" in row['Termék,szolgáltatás'].lower() or \
                "dérjuice" in row['Termék,szolgáltatás'].lower() or \
                "aperol spritz" in row['Termék,szolgáltatás'].lower() or \
                "7 up" in row['Termék,szolgáltatás'].lower() or \
                "lipton ice tea" in row['Termék,szolgáltatás'].lower() or \
                "fever tree tonic" in row['Termék,szolgáltatás'].lower() or \
                "toma eper 0,25l" in row['Termék,szolgáltatás'].lower() or \
                "egyszer használatos palack" in row['Termék,szolgáltatás'].lower() or \
                "gasztró" in row['Termék,szolgáltatás'].lower() or \
                "korsó" in row['Termék,szolgáltatás'].lower() or \
                ("kedvezmény" in row['Termék,szolgáltatás'].lower() and "27" in row['Termék,szolgáltatás'].lower()):
            df.at[index, "Tétel árbevétel főkönyv"] = "9122"
            df.at[index, "Tétel gazdasági esemény"] = "!32"
        elif "áru" in row['Termék,szolgáltatás'].lower() or "shop" in row['Termék,szolgáltatás'].lower():
            df.at[index, "Tétel árbevétel főkönyv"] = "9131"
            df.at[index, "Tétel gazdasági esemény"] = "!61"
        elif "egyéb" in row['Termék,szolgáltatás'].lower() or \
                "egyéb szolgáltatás" in row['Termék,szolgáltatás'].lower() or \
                "vízibicikli" in row['Termék,szolgáltatás'].lower() or \
                "vizibicikli" in row['Termék,szolgáltatás'].lower() or \
                "kerékpár" in row['Termék,szolgáltatás'].lower() or \
                "hajó" in row['Termék,szolgáltatás'].lower() or \
                ("óra" in row['Termék,szolgáltatás'].lower() and \
                    ("kajak" in row['Termék,szolgáltatás'].lower() or \
                     "kenu" in row['Termék,szolgáltatás'].lower() or \
                     "sup" in row['Termék,szolgáltatás'].lower())):
            df.at[index, "Tétel árbevétel főkönyv"] = "9115"
            df.at[index, "Tétel gazdasági esemény"] = "!21"
        elif "wellness" in row['Termék,szolgáltatás'].lower() or \
                "szauna" in row['Termék,szolgáltatás'].lower() or \
                "masszázs" in row['Termék,szolgáltatás'].lower() or \
                "maszázs" in row['Termék,szolgáltatás'].lower() or \
                "szolárium" in row['Termék,szolgáltatás'].lower():
            df.at[index, "Tétel árbevétel főkönyv"] = "9114"
            df.at[index, "Tétel gazdasági esemény"] = "!21"
        elif "apartman" in row['Termék,szolgáltatás'].lower():
            df.at[index, "Tétel árbevétel főkönyv"] = "9112"
            df.at[index, "Tétel gazdasági esemény"] = "!12"
        elif ifa[0].lower() in row['Termék,szolgáltatás'].lower() or ifa[1].lower() in row['Termék,szolgáltatás'].lower():
            df.at[index, "Tétel árbevétel főkönyv"] = "4694"
            
    #Rendezés
    df.sort_values(['Termék,szolgáltatás', 'Áfakulcs'], ascending=[True, True], inplace=True)
    
def ligetHotel(): 
    # List all files in the folder
    files = os.listdir(útvonal)

    # Filter out only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]
    
    if csv_files:
        # Assuming the first CSV file is the one you want to read
        for csv_file in csv_files:
            print(csv_file)
            # Construct the full path to the CSV file
            csv_file_path = os.path.join(útvonal, csv_file)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path, sep=";", encoding='ISO-8859-2')

            # Folder names to check
            folders_to_check = ["Hotel Felad"]
            for folder_name in folders_to_check:
                folder_path = os.path.join(útvonal, folder_name)
                if not os.path.exists(folder_path):
                    # Folder doesn't exist, create it
                    os.makedirs(folder_path)
                    print(f"The folder '{folder_name}' was created at {útvonal}.")
                else:
                    print(f"The folder '{folder_name}' already exists at {útvonal}.")
            
            
            if len(df) >= 2:
                új_név = df.at[1, "Számla kelte"]
                új_név = új_név.replace('.', '_')
                
                hotelezőMakró(df)
                    
                #Felad-ba
                df.to_csv(útvonal + "Hotel Felad\\" + új_név[:-1] + ".csv", index=False, encoding='ISO-8859-2', sep=";")
                os.startfile(útvonal + "Hotel Felad\\" + új_név[:-1] + ".csv")

                #Eredeti törlése
                for retry in range(10):
                    try:
                        os.remove(csv_file_path)
                        print("siker")
                        break
                    except:
                        print("deletion failed, retrying...")
            else:
                print("Üres csv")
    else:
        print("Nem található csv fájl a megadott mappában.")
    

def CaffeMakró(df):
    
    # To prevent dtype error
    df["Tétel árbevétel főkönyv"] = None
    df["Tétel árbevétel áfa"] = None
    df["Tétel gazdasági esemény"] = None
    df["Tétel áfa gazdasági esemény"] = None
    
    # Iterate through every row
    for index, row in df.iterrows():
        vevo_adoszam = row['Vevő adószám']

        #Adószám oszlop
        if pd.isna(vevo_adoszam):
            #print(f"NaN value found in row {index + 1}")
            df.at[index, "Vevő neve"] = "Magánszemély vevő"
            df.at[index, "Vevő irsz."] = None
            df.at[index, "Vevő város"] = None
            df.at[index, "Vevő utca"] = None
            # Add your actions for NaN values in each row
        #else:
            #print(f"Non-NaN value found in row {index + 1}: {vevo_adoszam}")
            # Add your actions for non-NaN values in each row
        
        
         
        #Áfakulcs oszlop
        if row["Áfakulcs"] == "ATK":
            df.at[index, "Tétel áfa gazdasági esemény"] = "ATHK"     
        else:
            df.at[index, "Tétel árbevétel áfa"] = "4671"
            if row["Áfakulcs"] == "27":
                df.at[index, "Tétel áfa gazdasági esemény"] = "27%"
            elif row["Áfakulcs"] == "5":
                substring = 'Előleg'
                if substring.lower() in row['Termék,szolgáltatás'].lower():
                    df.at[index, "Tétel áfa gazdasági esemény"] = "ELO5"
                else:
                    df.at[index, "Tétel áfa gazdasági esemény"] = "5%"
                    
        #Számlaszám: PAFR-xxxx-xxx
        if row["Számlaszám"].lower()[:2] == "pa":
            
            #Termék,szolgáltatás --> Tétel árbevétel főkönyv, Tétel gazdasági esemény
            ifa = ["ifa", "idegenforgalmi adó"]
            szervizdij = ["szervízdíj", "szervizdíj", "szervízdij", "szervizdij"]
            #szervízdíj
            if szervizdij[0] in row['Termék,szolgáltatás'].lower() or szervizdij[1] in row['Termék,szolgáltatás'].lower() or szervizdij[2] in row['Termék,szolgáltatás'].lower() or szervizdij[3] in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9123"
                df.at[index, "Tétel gazdasági esemény"] = "!11"
            elif "étel" in row['Termék,szolgáltatás'].lower() or \
                    "félpanzió" in row['Termék,szolgáltatás'].lower() or \
                    "étkezés" in row['Termék,szolgáltatás'].lower() or \
                    "reggeli" in row['Termék,szolgáltatás'].lower() or \
                    "ebéd" in row['Termék,szolgáltatás'].lower() or \
                    "vacsora" in row['Termék,szolgáltatás'].lower() or \
                    ("kedvezmény" in row['Termék,szolgáltatás'].lower() and "5" in row['Termék,szolgáltatás'].lower()):
                df.at[index, "Tétel árbevétel főkönyv"] = "9121"
                df.at[index, "Tétel gazdasági esemény"] = "!11"
            elif "jégkrém" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9121"
                df.at[index, "Tétel gazdasági esemény"] = "!32"
            elif "vital" in row['Termék,szolgáltatás'].lower(): 
                pass
            elif "ital" in row['Termék,szolgáltatás'].lower() or \
                    "pepsi" in row['Termék,szolgáltatás'].lower() or \
                    "liget víz" in row['Termék,szolgáltatás'].lower() or \
                    "limonádé" in row['Termék,szolgáltatás'].lower() or \
                    "toma prémium" in row['Termék,szolgáltatás'].lower() or \
                    "szent andrás" in row['Termék,szolgáltatás'].lower() or \
                    "szódavíz" in row['Termék,szolgáltatás'].lower() or \
                    "pohár" in row['Termék,szolgáltatás'].lower() or \
                    "cappuccino" in row['Termék,szolgáltatás'].lower() or \
                    "jeges kávé" in row['Termék,szolgáltatás'].lower() or \
                    "espresso" in row['Termék,szolgáltatás'].lower() or \
                    "hosszúlépés" in row['Termék,szolgáltatás'].lower() or \
                    "nagyfröccs" in row['Termék,szolgáltatás'].lower() or \
                    "szentkirályi szénsav" in row['Termék,szolgáltatás'].lower() or \
                    "schweppes" in row['Termék,szolgáltatás'].lower() or \
                    "dérjuice" in row['Termék,szolgáltatás'].lower() or \
                    "aperol spritz" in row['Termék,szolgáltatás'].lower() or \
                    "7 up" in row['Termék,szolgáltatás'].lower() or \
                    "lipton ice tea" in row['Termék,szolgáltatás'].lower() or \
                    "fever tree tonic" in row['Termék,szolgáltatás'].lower() or \
                    "toma eper 0,25l" in row['Termék,szolgáltatás'].lower() or \
                    "korsó" in row['Termék,szolgáltatás'].lower() or \
                    "palack" in row['Termék,szolgáltatás'].lower() or \
                    ("kedvezmény" in row['Termék,szolgáltatás'].lower() and "27" in row['Termék,szolgáltatás'].lower()):
                df.at[index, "Tétel árbevétel főkönyv"] = "9122"
                df.at[index, "Tétel gazdasági esemény"] = "!11"
            elif "terembérlet" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9124"
                df.at[index, "Tétel gazdasági esemény"] = "!11"
            elif "kedvezmény" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel gazdasági esemény"] = "!11"
            elif ifa[0].lower() in row['Termék,szolgáltatás'].lower() or ifa[1].lower() in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "4694"
        
      
        #Számlaszám: LC-xxxx-xxx
        elif row["Számlaszám"].lower()[:3] == "lc-":
            df.at[index, "Tétel gazdasági esemény"] = "!11"

      
        #Számlaszám: LCFR-xxxx-xxx
        else:
                  
            #Termék,szolgáltatás --> Tétel árbevétel főkönyv, Tétel gazdasági esemény
            ifa = ["ifa", "idegenforgalmi adó"]
            szervizdij = ["szervízdíj", "szervizdíj", "szervízdij", "szervizdij"]
            if "előleg" in row['Termék,szolgáltatás'].lower() or "egycélú" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "4531"
            elif "szállás" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9111"
                df.at[index, "Tétel gazdasági esemény"] = "!21"
            #szervízdíj
            elif szervizdij[0] in row['Termék,szolgáltatás'].lower() or szervizdij[1] in row['Termék,szolgáltatás'].lower() or szervizdij[2] in row['Termék,szolgáltatás'].lower() or szervizdij[3] in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9114"
                df.at[index, "Tétel gazdasági esemény"] = "!22"
            elif "étel" in row['Termék,szolgáltatás'].lower() or \
                    "félpanzió" in row['Termék,szolgáltatás'].lower() or \
                    "étkezés" in row['Termék,szolgáltatás'].lower() or \
                    "reggeli" in row['Termék,szolgáltatás'].lower() or \
                    "ebéd" in row['Termék,szolgáltatás'].lower() or \
                    "vacsora" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9112"
                df.at[index, "Tétel gazdasági esemény"] = "!22"
            elif "vital" in row['Termék,szolgáltatás'].lower() and "masszázs" in row['Termék,szolgáltatás'].lower(): 
                df.at[index, "Tétel árbevétel főkönyv"] = "9114"
                df.at[index, "Tétel gazdasági esemény"] = "!21"
            elif "ital" in row['Termék,szolgáltatás'].lower() or \
                    "pepsi" in row['Termék,szolgáltatás'].lower() or \
                    "liget víz" in row['Termék,szolgáltatás'].lower() or \
                    "limonádé" in row['Termék,szolgáltatás'].lower() or \
                    "toma prémium" in row['Termék,szolgáltatás'].lower() or \
                    "szent andrás" in row['Termék,szolgáltatás'].lower() or \
                    "szódavíz" in row['Termék,szolgáltatás'].lower() or \
                    "pohár" in row['Termék,szolgáltatás'].lower() or \
                    "cappuccino" in row['Termék,szolgáltatás'].lower() or \
                    "jeges kávé" in row['Termék,szolgáltatás'].lower() or \
                    "espresso" in row['Termék,szolgáltatás'].lower() or \
                    "hosszúlépés" in row['Termék,szolgáltatás'].lower() or \
                    "nagyfröccs" in row['Termék,szolgáltatás'].lower() or \
                    "szentkirályi szénsav" in row['Termék,szolgáltatás'].lower() or \
                    "schweppes" in row['Termék,szolgáltatás'].lower() or \
                    "dérjuice" in row['Termék,szolgáltatás'].lower() or \
                    "aperol spritz" in row['Termék,szolgáltatás'].lower() or \
                    "7 up" in row['Termék,szolgáltatás'].lower() or \
                    "lipton ice tea" in row['Termék,szolgáltatás'].lower() or \
                    "fever tree tonic" in row['Termék,szolgáltatás'].lower() or \
                    "korsó" in row['Termék,szolgáltatás'].lower() or \
                    "palack" in row['Termék,szolgáltatás'].lower() or \
                    "toma eper 0,25l" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9113"
                df.at[index, "Tétel gazdasági esemény"] = "!22"

            elif "áru" in row['Termék,szolgáltatás'].lower() or "shop" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9119"
                df.at[index, "Tétel gazdasági esemény"] = "!21"
            elif "egyéb" in row['Termék,szolgáltatás'].lower() or \
                    "szolgáltatások" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9119"
                df.at[index, "Tétel gazdasági esemény"] = "!21"
            elif "wellness" in row['Termék,szolgáltatás'].lower() or \
                    "szauna" in row['Termék,szolgáltatás'].lower() or \
                    "masszázs" in row['Termék,szolgáltatás'].lower() or \
                    "maszázs" in row['Termék,szolgáltatás'].lower() or \
                    "szolárium" in row['Termék,szolgáltatás'].lower() or \
                    "bérlés" in row['Termék,szolgáltatás'].lower() or \
                    "bérlet" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9119"
                df.at[index, "Tétel gazdasági esemény"] = "!21"
            elif "kedvezmény" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9111"
                df.at[index, "Tétel gazdasági esemény"] = "!21"
            elif ifa[0].lower() in row['Termék,szolgáltatás'].lower() or ifa[1].lower() in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "4694"
            elif "jégkrém" in row['Termék,szolgáltatás'].lower():
                df.at[index, "Tétel árbevétel főkönyv"] = "9112"
                df.at[index, "Tétel gazdasági esemény"] = "!22"
            
    #Rendezés       
    df.sort_values(['Termék,szolgáltatás', 'Áfakulcs'], ascending=[True, True], inplace=True)
    
def ligetCafe(): 
    # List all files in the folder
    files = os.listdir(útvonal)

    # Filter out only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]
    
    if csv_files:
        # Assuming the first CSV file is the one you want to read
        for csv_file in csv_files:
            print(csv_file)
            # Construct the full path to the CSV file
            csv_file_path = os.path.join(útvonal, csv_file)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path, sep=";", encoding='ISO-8859-2')

            # Folder names to check
            folders_to_check = ["Cafe Felad"]
            for folder_name in folders_to_check:
                folder_path = os.path.join(útvonal, folder_name)
                if not os.path.exists(folder_path):
                    # Folder doesn't exist, create it
                    os.makedirs(folder_path)
                    print(f"The folder '{folder_name}' was created at {útvonal}.")
                else:
                    print(f"The folder '{folder_name}' already exists at {útvonal}.")
            
            
            if len(df) >= 2:
                új_név = df.at[1, "Számla kelte"]
                új_név = új_név.replace('.', '_')
                
                CaffeMakró(df)
                    
                #Felad-ba
                df.to_csv(útvonal + "Cafe Felad\\" + új_név[:-1] + ".csv", index=False, encoding='ISO-8859-2', sep=";")
                os.startfile(útvonal + "Cafe Felad\\" + új_név[:-1] + ".csv")
                
                #Eredeti törlése
                for retry in range(10):
                    try:
                        os.remove(csv_file_path)
                        print("siker")
                        break
                    except:
                        print("deletion failed, retrying...")
            else:
                print("Üres csv")
    else:
        print("Nem található csv fájl a megadott mappában.")
    
    
    
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
    ligetHotel()
    
elif művelet == 2:
    ligetCafe()
    
        