# Copyright © 2022 | Made By: MostafaAbdelaziz "me@mmox.me" , Mohamed Ehab 
# -- coding: utf-8 -

#Essential Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

msg =" " # change this massage with the message you want
nms = []  # an empty list to append names later
nums = []  # an empty list to append numbers later
nums_with_no_WA = []  # an empty list to append numbers with no what'sApp
nums_with_no_WA_owner = []  # an empty list to append numbers with no what'sApp
wrong_nums = []  # an empty list to append non valid numbers
nums_wrong_owner = []

def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)

def send(num,name,url,msg):
    # make sure to correct the number to be foundable on what'sApp
    num = str(num)

    if len(num) > 9:
        if num.startswith('0'):
            num = '+2' + num
        elif num.startswith('1'):
            num = '+20' + num
        elif num.startswith('2'):
            num = '+' + num
        elif num.startswith('+2'):
            num = num
        else:
            wrong_nums.append(num)
            return

        msg_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'

        driver.get(url + num)

        try:
            time.sleep(3)
            element_presence(By.XPATH, msg_xpath, 30)
            time.sleep(3)
            txt_box = driver.find_element(By.XPATH, msg_xpath)
            txt_box.send_keys("**This is an Automated Massage Don't replay** Hi "+name+', '+msg)  # Customize this line to add the name to your message
            txt_box.send_keys("\n")
            time.sleep(6)  # This is just to avoid bad connection problems

        except:
            BOX = '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div'
            time.sleep(3)
            element_presence(By.XPATH, BOX, 30)
            time.sleep(3)
            nums_with_no_WA.append(num)
            nums_with_no_WA_owner.append(name)

    else:
        wrong_nums.append(num)
        nums_wrong_owner.append(name)


DATA = pd.read_csv("list.csv")  # put your excel workbook path here make sure it's CSV file


for cell in DATA['Name']:  # replace A with the names column, starting with A1
    nms.append(cell)
for cell in DATA['Phone']:  # replace B with the numbers column, starting with B1
    nums.append(cell)

al = dict(zip(nums, nms))  # zipping the two lists in a dictionary

url = 'https://web.whatsapp.com/send?phone='
link = 'https://web.whatsapp.com/'

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(link)

time.sleep(10)  # prepare your phone to scan the code in those 10 seconds

# prepare your phone to scan the code in those 10 seconds


start = 1
for num in al:  # loop to send to all the sheet
    send(num, al[num], url, msg)
    print(str(start)+" / "+str(len(al)))
    start += 1
    time.sleep(3)

nums_no_WA_excel = {"Name": nums_with_no_WA_owner, "Phone": nums_with_no_WA}
Wrong_nums = {"Name-Wrong": nums_wrong_owner, "Phone-Wrong": wrong_nums}

#Final Reports
Report1 = pd.DataFrame(nums_no_WA_excel)
Report2 = pd.DataFrame(Wrong_nums)
Report1.to_csv("NoWhatsapp.csv", encoding="UTF-8")
Report2.to_csv("wrong_nums.csv", encoding="UTF-8")
