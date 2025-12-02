import time as t

import pyautogui as gui

import pygetwindow as gw

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
    t.sleep(2)

def basicAttack():
    gui.press("1")
    t.sleep(1)
    gui.press("a")
    t.sleep(1)
    gui.press("s")
    t.sleep(1)
    gui.press("d")
    t.sleep(1)
    gui.press("f")
    t.sleep(1)
    gui.press("g")
    t.sleep(1)
    gui.press("h")
    t.sleep(1)
    gui.press("j")
    t.sleep(1)
    gui.press("k")
    t.sleep(1)
    gui.press("l")
    t.sleep(1)
    gui.press("q")
    t.sleep(1)
    gui.press("2")
    t.sleep(1)
    gui.press("a")
    t.sleep(1)
    gui.press("3")
    t.sleep(1)
    gui.press("d")
    t.sleep(1)
    gui.press("4")
    t.sleep(1)
    gui.press("g")
    t.sleep(1)
    gui.press("5")
    t.sleep(1)
    gui.press("j")
    t.sleep(1)
    gui.press("6")
    t.sleep(1)
    gui.press("l")
    t.sleep(1)
    gui.press("7")
    for loop in range(11):
        t.sleep(1)
        gui.press("w")

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
            basicAttack()
        case "attackFinished":
            gui.press("v")
        case "unknown":
            print("Waiting for known state...")
    t.sleep(1)