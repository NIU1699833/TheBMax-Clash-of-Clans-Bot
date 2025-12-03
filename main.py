import time as t
import pyautogui as gui
import pygetwindow as gw
import random
import pytesseract
import math as m

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

lightningLevel = 10
lightningCapacity = 11

def recogniseState():
    foundState = 0
    states = {"homeScreen": "images/homeAttack.png",
              "findMatch": "images/findMatch.png",
              "attackButton": "images/startAttack.png",
              "inAttack": "images/nextEnemy.png",
              "attackFinished": "images/returnHome.png"}
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

def basicAttack():
    dragonPositions = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "q"]
    hotkeys = ["2", "3", "4", "5", "6"]
    heroPositions = ["a", "d", "g", "j", "l"]
    airDefense(lightningLevel, lightningCapacity)
    gui.press("1")
    for i in dragonPositions:
        gui.press(i)
        randomSleep(0.5)
    currentPosition = 0
    for i in hotkeys:
        gui.press(i)
        randomSleep(0.25)
        gui.press(heroPositions[currentPosition])
        randomSleep(0.5)
        currentPosition += 1
    gui.press("7")
    for loop in range(11):
        randomSleep(0.1)
        gui.press("w")

def randomSleep(seconds):
    modifier = seconds * 0.1
    t.sleep(seconds + random.uniform(-modifier, modifier))

def goldAmount():
    gold = pytesseract.image_to_string(gui.screenshot(region=(140, 170, 170, 40)))
    gold = gold.replace("o", "0").replace("l", "1")
    f = filter(str.isdecimal, gold)
    gold = "".join(f)
    print("Found village with " + gold + " gold.")
    if gold == "":
        return 0
    else:
        return int(gold)

def airDefense(lightningLevel, lightningCapacity):
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
                gui.press("7")
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

def detectFullStorages():
    try:
        gui.locateOnScreen("images/goldStorage.png", confidence=0.9)
        print("Gold Storage Full. Checking Elixir Storage.")
        try:
            gui.locateOnScreen("images/elixirStorage.png", confidence=0.9)
            print("Elixir Storage is also full. Stopping script (to be replaced with switch account).")
            return 0
        except:
            print("Elixir Storage is not full. Proceeding to attack .")
            return 1
    except:
        print("Gold Storage is not full. Proceeding to attack loop.")
        return 1

def mainLoop():
    focusBluestacks()
    while detectFullStorages() == 1:
        currentStatus = recogniseState()
        match currentStatus:
            case "homeScreen":
                gui.press("z")
            case "findMatch":
                gui.press("x")
            case "attackButton":
                gui.press("c")
            case "inAttack":
                if goldAmount() > 750000:
                    basicAttack()
                else:
                    gui.press("b")
            case "attackFinished":
                gui.press("v")
            case "unknown":
                print("Waiting for known state...")
        randomSleep(1)

mainLoop()