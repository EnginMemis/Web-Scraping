from email.utils import decode_rfc2231
from operator import le
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import numpy as np
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver.exe"

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--incognito")

driver = webdriver.Chrome(PATH, chrome_options=chromeOptions)
driver.maximize_window()
driver.delete_all_cookies()


driver.get("https://arsiv.mackolik.com/Iddaa-Programi")

driver.implicitly_wait(10)

day = driver.find_element(By.XPATH,"/html/body/div[2]/div[4]/div[1]/div/table/tbody/tr[1]/td[3]/select[1]/option[7]")
day.click()

sleep(5)

playedMatch = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[1]/div/table/tbody/tr[2]/td/div[2]/input")
playedMatch.click()

sleep(2)


df = pd.read_excel("maclar.xlsx")

df = df.drop("Unnamed: 0", axis = 1)

newDf = pd.DataFrame(columns=["Home", "Away", "Skor", "1", "X", "2", "Alt", "Ust", "Final 1", "Final X", "Final 2", "Final Alt", "Final Ust"])

count = 0


matches = driver.find_elements(By.CLASS_NAME, "alt1")

for i in range(len(matches)):   
    list = []
    try:
        teams = matches[i].find_elements(By.CLASS_NAME, "iddaa-rows-style")
        home = teams[0].text
        away = teams[2].text
        skor = matches[i].find_element(By.CSS_SELECTOR, "#Tr2 > td:nth-child(10)")
        ms1 = matches[i].find_element(By.CLASS_NAME, "MS1")
        ms2 = matches[i].find_element(By.CLASS_NAME, "MS2")
        msX = matches[i].find_element(By.CLASS_NAME, "MSX")
        au1 = matches[i].find_element(By.CLASS_NAME, "AU1")
        au2 = matches[i].find_element(By.CLASS_NAME, "AU2")

        list.append(home)
        list.append(away)
        list.append(skor.text)
        list.append(ms1.text)
        list.append(msX.text)
        list.append(ms2.text)
        list.append(au1.text)
        list.append(au2.text)

        finalMs1 = 0
        finalMsX = 0
        finalMs2 = 0
        finalAlt = 0
        finalUst = 0

        homeSkor = int(skor.text.split("-")[0])
        awaySkor = int(skor.text.split("-")[1])

        if homeSkor > awaySkor:
            finalMs1 = 1
        elif homeSkor < awaySkor:
            finalMs2 = 1
        else:
            finalMsX = 1

        if homeSkor + awaySkor > 2:
            finalUst = 1
        else:
            finalAlt = 1

        list.append(finalMs1)
        list.append(finalMsX)
        list.append(finalMs2)
        list.append(finalAlt)
        list.append(finalUst)

        newDf.loc[count] = list
        count += 1

    except:
        print("hata")

matches = driver.find_elements(By.CLASS_NAME, "alt2")

for i in range(len(matches)):   
    list = []
    try:
        teams = matches[i].find_elements(By.CLASS_NAME, "iddaa-rows-style")
        home = teams[0].text
        away = teams[2].text
        skor = matches[i].find_element(By.CSS_SELECTOR, "#Tr2 > td:nth-child(10)")
        ms1 = matches[i].find_element(By.CLASS_NAME, "MS1")
        ms2 = matches[i].find_element(By.CLASS_NAME, "MS2")
        msX = matches[i].find_element(By.CLASS_NAME, "MSX")
        au1 = matches[i].find_element(By.CLASS_NAME, "AU1")
        au2 = matches[i].find_element(By.CLASS_NAME, "AU2")

        list.append(home)
        list.append(away)
        list.append(skor.text)
        list.append(ms1.text)
        list.append(msX.text)
        list.append(ms2.text)
        list.append(au1.text)
        list.append(au2.text)

        finalMs1 = 0
        finalMsX = 0
        finalMs2 = 0
        finalAlt = 0
        finalUst = 0

        homeSkor = int(skor.text.split("-")[0])
        awaySkor = int(skor.text.split("-")[1])

        if homeSkor > awaySkor:
            finalMs1 = 1
        elif homeSkor < awaySkor:
            finalMs2 = 1
        else:
            finalMsX = 1

        if homeSkor + awaySkor > 2:
            finalUst = 1
        else:
            finalAlt = 1

        list.append(finalMs1)
        list.append(finalMsX)
        list.append(finalMs2)
        list.append(finalAlt)
        list.append(finalUst)

        newDf.loc[count] = list
        count += 1

    except:
        print("Error")

df3 = pd.concat([df, newDf], axis = 0, ignore_index=True)
df3.reset_index()
df3.to_excel("yeniMaclar.xlsx")
driver.quit()

