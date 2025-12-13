# TheBMax Clash of Clans Bot

An automated Python bot for farming resources in Clash of Clans using BlueStacks. It utilizes computer vision (`pyautogui`, `pytesseract`) to detect game states, identify full storages, and perform attacks using lightning spells on Air Defenses.

## Features
* **Multi-Account Support:** Automatically cycles through 11 distinct accounts.
* **Smart Farming:** skips bases with low gold; detects full storages to switch accounts.
* **Auto-Attack Logic:**
    * Calculates required lightning spells for Air Defenses.
    * Deploys troops and heroes based on custom keybind profiles.
* **OCR Integration:** Reads gold values from the screen.

## Requirements
* Python 3.x
* BlueStacks App Player (1920x1080 resolution recommended)
* Tesseract OCR

## Setup
1.  Install dependencies: `pip install pyautogui pygetwindow pytesseract opencv-python`
2.  Configure `tesseract_cmd` path in the script.
3.  Ensure your `images/` folder contains the required reference screenshots (Air Defenses, UI buttons, Profile icons).