import time as t
import pyautogui as gui
import pygetwindow as gw
import random
import pyscreeze
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def recogniseState():
    try:
        gui.locateOnScreen("images/homeAttack.png", confidence=0.9)
        print("Current Status: Home Screen")
        return "homeScreen"
    except gui.ImageNotFoundException:
        try:
            gui.locateOnScreen("images/findMatch.png", confidence=0.9)
            print("Current Status: Find a Match Button")
            return "findMatch"
        except gui.ImageNotFoundException:
            try:
                gui.locateOnScreen("images/startAttack.png", confidence=0.9)
                print("Current Status: Attack Button")
                return "attackButton"
            except gui.ImageNotFoundException:
                try:
                    gui.locateOnScreen("images/nextEnemy.png", confidence=0.9)
                    print("Current Status: In Attack")
                    return "inAttack"
                except gui.ImageNotFoundException:
                    try:
                        gui.locateOnScreen("images/returnHome.png", confidence=0.9)
                        print("Current Status: Attack Finished")
                        return "attackFinished"
                    except gui.ImageNotFoundException:
                        print("Unknown State")
                        return "unknown"

def focusBluestacks():
    gw.getWindowsWithTitle("BlueStacks App Player")[0].activate()
    randomSleep(2)

def basicAttack():
    dragonPositions = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "q"]
    hotkeys = ["2", "3", "4", "5", "6"]
    heroPositions = ["a", "d", "g", "j", "l"]
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
    return int(gold)

def mainLoop():
    focusBluestacks()
    while True:
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