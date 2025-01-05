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