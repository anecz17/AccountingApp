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

    
def ligetHotel(útvonal=None): 
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
            
            
            #Letöltött-be berakom az eredetit
            if len(df) >= 2:
                új_név = df.at[1, "Számla kelte"]
                új_név = új_név.replace('.', '_')
                
                hotelezőMakró(df)
                    
                #Felad-ba
                df.to_csv(útvonal + "Hotel Felad\\" + új_név[:-1] + ".csv", index=False, encoding='ISO-8859-2', sep=";")
                os.startfile(útvonal + "Hotel Felad\\" + új_név[:-1] + ".csv")

                #Eredeti törlése
                os.remove(csv_file_path)
            else:
                print("Üres csv")
    else:
        print("Nem található csv fájl a megadott mappában.")
    


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