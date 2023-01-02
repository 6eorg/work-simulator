import glob
import os
import time
import random
from datetime import datetime

import pyautogui
import pyperclip

# CONFIGURATION
addresses_f = ["Sehr geehrte Frau", "Liebe Frau"]
addresses_m = ["Sehr geehrter Herr", "Lieber Herr"]
names = ["Meier", "Müller", "Huber", "Hugentobler", "Ramseier", "Schneider"]
fileNameLetter = "Brief"
fileNameGender = ["Herr", "Frau"]
yourName = "Georg"
save_directory = "geschriebene_Briefe"

MIN_TYPE_SPEED = 0.0001
MAX_TYPE_SPEED = 0.1
ERROR_RATE = 10  # error every x char (average)


# creates directory to save the written letters
def createDirectoryAndTemplate(directoryName):
    if not os.path.exists('./' + directoryName):
        os.makedirs('./' + directoryName)
    # create empty file (template) if no existing template
    try:
        open(directoryName + "/template.txt", "x")
    except:
        print("File already exists")


# read and return the texts from text files in the 'letters' directory
def readLetters():
    letters_path = glob.glob("./letters/*.txt")
    letters = []
    for path in letters_path:
        text = ""
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                text = text + line
        letters.append(text)
    return letters

# simulates keystrokes
def typeText(text):
    writtenText = ""
    for char in text:
        pyperclip.copy(char)
        writtenText = writtenText + char
        rand = random.randint(0, ERROR_RATE)
        typeSpeed = round(random.uniform(MIN_TYPE_SPEED, MAX_TYPE_SPEED), 4)
        if (rand == 1 and len(writtenText) > 5):
            # CORRECT TEXT
            time.sleep(typeSpeed)
            # write two random chars
            errors = [*"abcdefgihijklmnopqrstuvwxyzABCDEFG0123456"]
            pyautogui.write(random.choice(errors), typeSpeed)
            pyautogui.write(random.choice(errors), typeSpeed)
            # delete the chars
            pyautogui.press('backspace')
            time.sleep(typeSpeed + 0.1)
            pyautogui.press('backspace')
            time.sleep(typeSpeed + 0.1)
            # write the right one
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(typeSpeed)
        else:
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(typeSpeed)


# SETUP
createDirectoryAndTemplate(save_directory)
letters = readLetters()

while True:
    # Preparations
    letter = random.choice(letters)
    gender = random.choice(["f", "m"])
    name = random.choice(names)
    address = random.choice(addresses_f if gender == "f" else addresses_m)
    fileAddress = fileNameGender[0] if gender == "f" else fileNameGender[1]
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + fileNameLetter + "_" + fileAddress + "_" + name + ".txt"

    # open template (editor)
    os.startfile(os.getcwd() + '\\' + save_directory + '\\template.txt')
    time.sleep(4)

    # write Address
    letter_address = address + " " + name + "\n\n"
    typeText(letter_address)

    # write text
    typeText(letter)

    # write signature
    typeText("\n" + yourName)

    # save file
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'shift', 's')
    typeText(filename)
    pyautogui.press('enter')

    # close file
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(3)