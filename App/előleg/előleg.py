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


def előleg(útvonal=None): 
    # List all files in the folder
    files = os.listdir(útvonal)

    # Filter out only CSV files
    excel_files = [file for file in files if file.endswith('.xlsx')]
    
    if excel_files:
        # Assuming the first CSV file is the one you want to read
        for excel_file in excel_files:
            print(excel_file)
            # Construct the full path to the CSV file
            excel_file_path = os.path.join(útvonal, excel_file)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_excel(excel_file_path)

            # Folder names to check
            folders_to_check = ["Előleg"]
            for folder_name in folders_to_check:
                folder_path = os.path.join(útvonal, folder_name)
                if not os.path.exists(folder_path):
                    # Folder doesn't exist, create it
                    os.makedirs(folder_path)
                    print(f"The folder '{folder_name}' was created at {útvonal}.")
                else:
                    print(f"The folder '{folder_name}' already exists at {útvonal}.")
            
            pass
            #Letöltött-be berakom az eredetit
            if len(df) >= 2:
                új_név = df.at[1, "Könyvelés dátuma"]
                új_név = új_név.replace('.', '_')
                
                # Feldolgozás
                másolat, df = előlegező(df)
                    
                with pd.ExcelWriter(útvonal + "Előleg\\" + új_név[:-1] + ".xlsx") as writer:
                    df.to_excel(writer, sheet_name="pártalan", index=False)
                    másolat.to_excel(writer, sheet_name="párban", index=False)
                    
                os.startfile(útvonal + "Előleg\\" + új_név[:-1] + ".xlsx")

                #Eredeti törlése
                os.remove(excel_file_path)
            else:
                print("Üres excel")
    else:
        print("Nem található excel fájl a megadott mappában.")
    


def előlegező(df):
    # megegyezik bármelyik korábbival
    
    duplicates = pd.DataFrame(columns=df.columns)
    print(duplicates)
    to_delete = []
    
    df = df.sort_values(by='Követel HUF', ascending=True)
    df['Közös'] = df["Követel HUF"]
    df.loc[df['Közös'].isnull(), 'Közös'] = df['Tartozik HUF']
    df = df.sort_values(by='Közös', ascending=True)
    df = df.reset_index(drop=True)

    for index1, row1 in df.iterrows():
        print(index1, len(to_delete))
        for index2, row2 in df.iterrows():
            if index1 >= index2:
                continue
            if index2 in to_delete:
                continue
            if row1["Követel HUF"] == row2["Tartozik HUF"] or row2["Követel HUF"] == row1["Tartozik HUF"]:
                if str(row1["Számla száma"]) in str(row2["Leírás"]) or str(row2["Számla száma"]) in str(row1["Leírás"]):
                    duplicates = pd.concat([duplicates, df.iloc[[index1]], df.iloc[[index2]]], ignore_index=True)
                    to_delete.append(index1)
                    to_delete.append(index2)
            elif row1["Közös"] < row2["Közös"]:
                break
                    
    
    to_delete.sort(reverse=True)
    
    df = df.drop(to_delete, axis=0).reset_index(drop=True)
    
    return duplicates, df
    
    
                
                
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