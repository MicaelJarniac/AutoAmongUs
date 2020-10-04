import cv2 as cv
import numpy as np
from mss import mss


def draw_box(img, bbox):
    x, y, w, h = (int(v) for v in bbox)
    cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3, 1)


def draw_text(img, text, type):
    pos = (0, 0)
    color = (255, 255, 255)
    if type == "fps":
        pos = (25, 25)
    elif type == "err":
        pos = (25, 50)
        color = (0, 0, 255)
    elif type == "success":
        pos = (25, 50)
        color = (0, 255, 0)
    cv.putText(
        img,
        text,
        pos,
        cv.FONT_HERSHEY_PLAIN,
        1.0,
        color,
        1,
    )


def draw_fps(img, fps):
    draw_text(img, f"{int(fps)} FPS", "fps")


with mss() as sct:
    tracker = cv.TrackerMOSSE_create()
    # tracker = cv.TrackerCSRT_create()
    img = np.array(sct.grab(sct.monitors[0]))
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)
    bbox = cv.selectROI("Screen", img, False)
    tracker.init(img, bbox)

    while True:
        timer = cv.getTickCount()
        img = np.array(sct.grab(sct.monitors[0]))
        img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

        success, bbox = tracker.update(img)

        if success:
            draw_box(img, bbox)
            draw_text(img, "Tracking", "success")
        else:
            draw_text(img, "Lost", "err")

        fps = cv.getTickFrequency() / (cv.getTickCount() - timer)
        draw_fps(img, fps)
        cv.imshow("Screen", img)

        if cv.waitKey(1) == 27:
            break

cv.destroyAllWindows()
