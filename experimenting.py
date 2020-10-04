import time

import pyautogui

from autoamongus.tasks import DivertPower, EmptyGarbage, SwipeCard

if __name__ == "__main__":
    time.sleep(3)
    for _ in range(5):
        pyautogui.press("space")
        time.sleep(1)
        img = pyautogui.screenshot()
        task = DivertPower(img)
        task.execute()
        time.sleep(1)
