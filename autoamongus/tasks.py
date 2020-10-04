import time
from functools import cached_property
from typing import Tuple

import cv2 as cv
import numpy as np
import pyautogui

from autoamongus.utils import get_pos


class DetectTask:
    def __init__(self):
        self.task = None


class Task:
    area = (1920, 1080)


class SwipeCard(Task):
    def __init__(self):
        self.swipe_time: float = 1.1
        # self.card_start: tuple = (770, 880)
        self._card_start: Tuple[float, float] = (0.4, 0.8)
        # self.swipe_start: tuple = (500, 400)
        self._swipe_start: Tuple[float, float] = (0.25, 0.35)
        # self.swipe_len: int = 1000
        self._swipe_len: Tuple[float, float] = (0.5, 0.0)
        self.swipe_delay: float = 0.4

    @cached_property
    def card_start(self):
        return get_pos(self._card_start, self.area)

    @cached_property
    def swipe_start(self):
        return get_pos(self._swipe_start, self.area)

    @cached_property
    def swipe_len(self):
        return get_pos(self._swipe_len, self.area)

    def execute(self):
        pyautogui.click(self.card_start)
        time.sleep(self.swipe_delay)
        pyautogui.moveTo(self.swipe_start)
        pyautogui.drag(*self.swipe_len, self.swipe_time)


class EmptyGarbage(Task):
    def __init__(self):
        # self.lever_start: tuple = (1275, 420)
        self._lever_start: Tuple[float, float] = (0.65, 0.4)
        # self.lever_len: int = 400
        self._lever_len: Tuple[float, float] = (0.0, 0.4)
        self.lever_time: float = 0.4
        self.lever_hold: float = 1.1

    @cached_property
    def lever_start(self):
        return get_pos(self._lever_start, self.area)

    @cached_property
    def lever_len(self):
        return get_pos(self._lever_len, self.area)

    def execute(self):
        pyautogui.mouseDown(self.lever_start)
        pyautogui.move(*self.lever_len, self.lever_time)
        time.sleep(self.lever_hold)
        pyautogui.mouseUp()


class DivertPower(Task):
    def __init__(self, img):
        img = np.array(img)
        img = cv.cvtColor(img, cv.COLOR_RGBA2BGR)
        self.img = img
        self._faders_bounds: Tuple[Tuple[float, float], Tuple[float, float]] = (
            (0.3, 0.7),
            (0.7, 0.76),
        )
        self._drag_len: Tuple[float, float] = (0.0, -0.15)
        self.drag_time: float = 0.2

    @cached_property
    def drag_len(self):
        return get_pos(self._drag_len, self.area)

    @cached_property
    def faders_bounds(self):
        return tuple(get_pos(corner, self.area) for corner in self._faders_bounds)

    @cached_property
    def faders(self):
        img = self.img
        p1, p2 = self.faders_bounds
        x, y = p1
        x2, y2 = p2
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        mask[y:y2, x:x2] = 255
        img = cv.bitwise_and(img, img, mask=mask)
        return img

    @cached_property
    def active_fader(self):
        roi = self.faders
        roi = np.array([[r for b, g, r in p] for p in roi])
        roi = cv.GaussianBlur(roi, (51, 51), 0)
        *_, max = cv.minMaxLoc(roi)
        return max

    def execute(self):
        pyautogui.moveTo(self.active_fader)
        pyautogui.drag(*self.drag_len, self.drag_time)


# 580, 755 / 0.3, 0.7
# 1340, 820 / 0.7, 0.76
