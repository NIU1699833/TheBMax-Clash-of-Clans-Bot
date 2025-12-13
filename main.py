import time as t
import pyautogui as gui
import pygetwindow as gw
import random
import pytesseract
import math as m

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PROFILES = {
    "TheBMax1": {
        "minGold": 750000,
        "lightningLevel": 10,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3", "4"],
        "heroBinds": ["5", "6", "7", "8", "9"],
        "spellBind": "0"
    },
    "TheBMax2": {
        "minGold": 750000,
        "lightningLevel": 9,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3"],
        "heroBinds": ["4", "5", "6", "7", "8"],
        "spellBind": "9"
    },
    "TheBMax3": {
        "minGold": 750000,
        "lightningLevel": 9,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3", "4"],
        "heroBinds": ["5", "6", "7", "8", "9"],
        "spellBind": "0"
    },
    "TheBMax4": {
        "minGold": 750000,
        "lightningLevel": 9,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3"],
        "heroBinds": ["4", "5", "6", "7", "8"],
        "spellBind": "9"
    },
    "TheBMax5": {
        "minGold": 750000,
        "lightningLevel": 9,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3"],
        "heroBinds": ["4", "5", "6", "7", "8"],
        "spellBind": "9"
    },
    "TheBMax6": {
        "minGold": 750000,
        "lightningLevel": 9,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3"],
        "heroBinds": ["4", "5", "6", "7"],
        "spellBind": "8"
    },
    "TheBMax7": {
        "minGold": 500000,
        "lightningLevel": 8,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3", "4"],
        "heroBinds": ["4", "5", "6", "7", "8"],
        "spellBind": "9"
    },
    "TheBMax8": {
        "minGold": 500000,
        "lightningLevel": 7,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3", "4"],
        "heroBinds": ["5", "6", "7"],
        "spellBind": "8"
    },
    "TheBMax9": {
        "minGold": 500000,
        "lightningLevel": 7,
        "lightningCapacity": 11,
        "troopBinds": ["1", "2", "3"],
        "heroBinds": ["4", "5"],
        "spellBind": "6"
    },
    "TheBMax10": {
        "minGold": 250000,
        "lightningLevel": 6,
        "lightningCapacity": 9,
        "troopBinds": ["1", "2", "3"],
        "heroBinds": ["4", "5"],
        "spellBind": "6"
    },
    "TheBMax11": {
        "minGold": 250000,
        "lightningLevel": 5,
        "lightningCapacity": 7,
        "troopBinds": ["1", "2", "3"],
        "heroBinds": ["4"],
        "spellBind": "5"
    }
}

currentProfile = "TheBMax11"
profileData = PROFILES[currentProfile]

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

def basicAttack(profileData):
    positions = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "q"]
    heroPositions = ["a", "d", "g", "j", "l"]
    airDefense(profileData["lightningLevel"], profileData["lightningCapacity"], profileData)
    for troop in profileData["troopBinds"]:
        gui.press(troop)
        for i in positions:
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

def detectFullStorages():
    if gui.pixelMatchesColor(1474, 83, (244, 221, 114)) and gui.pixelMatchesColor(1474, 173, (225, 141, 225)):
        print("Gold and Elixir Storages are full. Going Idle / Switching Accounts")
        return 0
    else:
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
                if goldAmount() > profileData["minGold"]:
                    basicAttack(profileData)
                else:
                    gui.press("b")
            case "attackFinished":
                gui.press("v")
            case "unknown":
                print("Waiting for known state...")
        randomSleep(1)

mainLoop()