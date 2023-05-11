import cv2
import hand as htm
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=1)

while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(frame, (x1, y1), 15, (255, 0, 255), -1)
        cv2.circle(frame, (x2, y2), 15, (255, 0, 255), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)

        if length < 25:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(frame, (cx, cy), 15, (0, 255, 255), -1)

        vol = np.interp(length, [25, 225], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        volBar = np.interp(length, [25, 225], [200, 450])
        vol_tyle = np.interp(length, [25, 225], [0, 100])
        cv2.rectangle(frame, (200, 420), (450, 450), (160, 160, 160), -1)
        cv2.rectangle(frame, (200, 420), (int(volBar), 450), (250, 190, 110), -1)
        cv2.putText(frame, f"{int(vol_tyle)}%", (300, 445), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()