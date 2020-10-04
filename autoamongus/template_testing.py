import cv2 as cv
import numpy as np


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


# template = cv.imread("autoamongus/assets/tasks/card/card.png", cv.IMREAD_GRAYSCALE)
template = cv.imread("autoamongus/assets/tasks/card/card.png", cv.IMREAD_GRAYSCALE)
# img = cv.imread("autoamongus/assets/tasks/card/card.png")
img = cv.imread("autoamongus/assets/test/swipe_card_4.png", cv.IMREAD_GRAYSCALE)
# img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# orb = cv.ORB_create()
# kp1, des1 = orb.detectAndCompute(template, None)
# kp2, des2 = orb.detectAndCompute(img, None)
#
# bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
#
# matches = bf.match(des1, des2)
# matches = sorted(matches, key=lambda x: x.distance)
#
# img3 = cv.drawMatches(template, kp1, img, kp2, matches[:30], None, flags=2)

found = 0
scale = 0.1
threshold = 0.7
while found < 1:
    scale += 0.1
    template_resized = cv.resize(
        template, tuple((int(d * scale) for d in template.shape[:2][::-1]))
    )
    # cv.imshow("Template", template_resized)

    res = cv.matchTemplate(img, template_resized, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        *_, w, h = template_resized.shape[::-1]
        cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        found += 1

print(scale)

cv.imshow("Image", img)
cv.waitKey(0)
cv.destroyAllWindows()
