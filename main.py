import time as t
import pyautogui as gui
import pygetwindow as gw
import random
import pytesseract
import math as m
from config import PROFILES
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def recogniseState():
    foundState = 0
    states = {"Home Screen": "images/homeAttack.png",
              "Find Match": "images/findMatch.png",
              "Attack Button": "images/startAttack.png",
              "In Attack": "images/nextEnemy.png",
              "Attack Finished": "images/returnHome.png",
              "Reload Game": "images/reloadGame.png",
              "Connection Lost": "images/tryAgain.png"}
    for state in states:
        try:
            gui.locateOnScreen(states[state], confidence=0.9)
            print("Current Status: " + state)
            foundState = state
            return foundState
        except gui.ImageNotFoundException:
            continue
    if foundState == 0:
        return "unknown"
    else:
        return foundState

def focusBluestacks():
    gw.getWindowsWithTitle("BlueStacks App Player")[0].activate()
    randomSleep(2)

def basicAttack(profileData):
    heroPositions = ["a", "d", "g", "j", "l"]
    gui.keyDown("o")
    randomSleep(0.5)
    gui.keyUp("o")
    lightningRemaining = airDefense(profileData["lightningLevel"], profileData["lightningCapacity"], profileData)
    for troop in profileData["troopBinds"]:
        gui.press(troop)
        for i in profileData["positions"]:
            gui.press(i)
            randomSleep(0.5)
    currentPosition = 0
    for i in profileData["heroBinds"]:
        gui.press(i)
        randomSleep(0.25)
        gui.press(heroPositions[currentPosition])
        randomSleep(0.5)
        currentPosition += 1
    gui.press(profileData["spellBind"])
    for loop in range(lightningRemaining):
        randomSleep(0.1)
        gui.press("w")

def randomSleep(seconds):
    modifier = seconds * 0.1
    t.sleep(seconds + random.uniform(-modifier, modifier))

def goldAmount():
    gold = pytesseract.image_to_string(gui.screenshot(region=(100, 150, 160, 40)))
    gold = gold.replace("o", "0").replace("l", "1")
    f = filter(str.isdecimal, gold)
    gold = "".join(f)
    print("Found village with " + gold + " gold.")
    if gold == "":
        return 0
    else:
        return int(gold)

def airDefense(lightningLevel, lightningCapacity, data):
    lightningDamage = [150, 180, 210, 240, 270, 320, 400, 480, 560, 600, 640, 680, 720]
    airDefenseHealth = [800, 850, 900, 950, 1000, 1050, 1100, 1210, 1300, 1400, 1500, 1650, 1750, 1850, 1950, 2000]
    lowestLevelNotFound = 0
    while (lightningCapacity > 0) and (lowestLevelNotFound < 15):
        lowestLevelNotFound = 0
        for defense in range(1, 16):
            try:
                x, y = gui.locateCenterOnScreen(f"images/airDefense/level{defense}.png", confidence=0.9)
                print(f"Found Air Defense level {defense} at {x}, {y}")
                lightningNeeded = m.ceil(airDefenseHealth[defense] / lightningDamage[lightningLevel - 1])
                print(f"Deploying {lightningNeeded} lightning spells at {x}, {y}")
                gui.press(data["spellBind"])
                for spell in range(1, lightningNeeded + 1):
                    gui.click(x, y)
                    randomSleep(0.25)
                    lightningCapacity -= 1
                break
            except gui.ImageNotFoundException:
                lowestLevelNotFound += 1
                print(f"Couldn't find air defense level {defense}")
                continue
        print(lowestLevelNotFound)
    return lightningCapacity

def detectFullStorages():
    if gui.pixelMatchesColor(1474, 83, (244, 221, 114)) and gui.pixelMatchesColor(1474, 173, (225, 141, 225)):
        print("Gold and Elixir Storages are full. Going Idle / Switching Accounts")
        return 0
    else:
        return 1

def waitToFind(imagePath):
    found = False
    while not found:
        try:
            gui.locateOnScreen(imagePath, confidence=0.9)
            found = True
        except gui.ImageNotFoundException:
            print(f"Could not find {imagePath}. Waiting one second.")
            randomSleep(1)

def switchAccounts(desiredProfile):
    attempts = 0
    found = False
    waitToFind("images/homeAttack.png")
    gui.press("n")
    randomSleep(0.5)
    gui.press("m")
    waitToFind("images/switchAccountMenu.png")
    randomSleep(1)

    found = False
    while not found and attempts < 20:
        try:
            x, y = gui.locateCenterOnScreen(f"images/profiles/{desiredProfile}.png", confidence=0.9)
            gui.moveTo((x, y))
            gui.click(x, y)
            found = True
        except gui.ImageNotFoundException:
            gui.press("p")
            gui.press("p")
            gui.press("p")
            randomSleep(0.5)
            attempts += 1
            continue
    if not found:
        print(f"CRITICAL: Could not find profile {desiredProfile}. Stopping script (in future, add logic to restart game)")

def locateAndClick(imagePath):
    found = False
    x, y = 0, 0
    while not found:
        try:
            x, y = gui.locateCenterOnScreen(imagePath, confidence=0.9)
            found = True
        except gui.ImageNotFoundException:
            print(f"Could not find image {imagePath}. Waiting one second.")
            randomSleep(1)
    gui.click(x, y)

def openBluestacks():
    if not gw.getWindowsWithTitle("BlueStacks App Player"):
        os.startfile(r"C:\Users\Max\Desktop\Clash of Clans.lnk")
        randomSleep(5)
        focusBluestacks()
        waitToFind("images/homeAttack.png")
        print("Clash of Clans Opened!")
    else:
        closeBluestacks()
        randomSleep(2)
        openBluestacks()

def closeBluestacks():
    if gw.getWindowsWithTitle("BlueStacks App Player")[0]:
        os.system("taskkill /f /im HD-Player.exe")
        print("Closed Bluestacks!")
    else:
        print("Bluestacks is not open!")


def attackLoop(profileData):
    while detectFullStorages() == 1:
        currentStatus = recogniseState()
        match currentStatus:
            case "Home Screen":
                gui.press("z")
            case "Find Match":
                gui.press("x")
            case "Attack Button":
                gui.press("c")
            case "In Attack":
                if goldAmount() > profileData["minGold"]:
                    basicAttack(profileData)
                else:
                    gui.press("b")
            case "Attack Finished":
                gui.press("v")
            case "Reload Game":
                locateAndClick("images/reloadGame.png")
            case "Connection Lost":
                locateAndClick("images/tryAgain.png")
            case "unknown":
                print("Waiting for known state...")
        randomSleep(1)

def mainLoop():
    openBluestacks()
    startAccount = 1
    endAccount = 10
    accountNumber = startAccount
    focusBluestacks()
    while accountNumber <= endAccount:
        switchAccounts(f"TheBMax{accountNumber}")
        profileData = PROFILES[f"TheBMax{accountNumber}"]
        print(f"Attacking on profile TheBMax{accountNumber}")
        randomSleep(5)
        attackLoop(profileData)
        accountNumber += 1

mainLoop()