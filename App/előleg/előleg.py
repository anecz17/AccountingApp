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
    skip = []
    
    df = df.sort_values(by='Követel HUF', ascending=True)
    df['Közös'] = df["Követel HUF"]
    df.loc[df['Tartozik HUF'] > 0, 'Közös'] = df['Tartozik HUF']
    df = df.sort_values(by='Közös', ascending=True)
    df = df.reset_index(drop=True)
    print(df)

    for index1, row1 in df.iterrows():
        print(index1, len(to_delete))
        if index1 in skip or index1 in to_delete:
            continue
        for index2, row2 in df.iterrows():
            if index2 in to_delete or index2 in skip:
                continue
            if row1["Közös"] == row2["Közös"]: # or row2["Követel HUF"] == row1["Tartozik HUF"]:
                if str(row1["Számla száma"]) in str(row2["Leírás"]) or str(row2["Számla száma"]) in str(row1["Leírás"]):
                    if rec_check(df, to_delete, index1, index2, row1, row2):
                        duplicates = pd.concat([duplicates, df.iloc[[index1]], df.iloc[[index2]]], ignore_index=True)
                        to_delete.append(index1)
                        to_delete.append(index2)
                    else:
                        # skip all rows that have share the same számlaszám
                        for index3, row3 in df.iterrows():
                            if str(row1["Számla száma"]) in str(row3["Leírás"]) or str(row3["Számla száma"]) in str(row1["Leírás"]):
                                skip.append(index3)
                        break
            elif row1["Közös"] < row2["Közös"]:
                break
                    
    
    to_delete.sort(reverse=True)
    
    df = df.drop(to_delete, axis=0).reset_index(drop=True)
    
    return duplicates, df

def rec_check(df, to_delete, pind1, pind2, prow1, prow2):
    match = True
    print("in rec_check for index: ", pind1)
    for index1, row1 in df.iterrows():
        if index1 <= pind1 or index1 == pind2:
            continue
        if row1["Közös"] != prow1["Közös"]:
            continue
        if str(row1["Számla száma"]) in str(prow1["Leírás"]) or str(prow1["Számla száma"]) in str(row1["Leírás"]) or str(row1["Számla száma"]) in str(prow2["Leírás"]) or str(prow2["Számla száma"]) in str(row1["Leírás"]):
            print("more checking")
            for index2, row2 in df.iterrows():
                
                if row2["Közös"] != row1["Közös"]:
                    match = False
                    continue
                if index2 <= pind1 or index2 == pind2:
                    continue
                if str(row1["Számla száma"]) in str(row2["Leírás"]) or str(row2["Számla száma"]) in str(row1["Leírás"]):
                    match = True
                    return rec_check(df, to_delete, index1, index2, row1, row2)

    print(match)  
    return match