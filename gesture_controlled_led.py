#CODE FOR GESTURE LED PROJECT // RANCHO LABS// ARNAV GARG //
#1 IMPORTING NECESSARY LIBRARIES
import cv2
import mediapipe as mp
import time
import ArduinoCode as ac
 #INITIALIZE MEDIAPIPE HANDS MODULE
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
# DEFINE THE FINGERTIP IDS FOR HAND TRACKING
tipIds = [4, 8, 12, 16, 20]
# OPEN VIDEO CAPTURE
video = cv2.VideoCapture(0)
# SET UP ARDUINO BOARD
comport = 'COM3'
board = pyfirmata.Arduino(comport)
leds = [board.get_pin(f'd:{pin}:o') for pin in range(13, 8, -1)]
# DEFINE LED CONTROL FUNCTION
def led(total):
 for i, pin in enumerate(leds):
 pin.write(1 if i < total else 0)
 )
# MAIN LOOP FOR HAND TRACKING AND LED CONTROL
with mp_hand.Hands
(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
 while True:
 # READ FRAME FROM VIDEO CAPTURE
 ret, image = video.read()
 image = cv2.cvtColor(image,
cv2.COLOR_BGR2RGB)
# PROCESS HAND LANDMARKS USING MEDIAPIPE
 results = hands.process(image)
 image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
 lmList = []
# PROCESS DETECTED HAND LANDMARKS
 if results.multi_hand_landmarks:
 myHands = results.multi_hand_landmarks[0]
 for id, lm in enumerate(myHands.landmark):
 h, w, c = image.shape
 cx, cy = int(lm.x * w), int(lm.y * h)
 lmList.append([id, cx, cy])
 mp_draw.draw_landmarks(image, myHands,
mp_hand.HAND_CONNECTIONS)
# DETECT FINGER STATES BASED ON LANDMARK POSITIONS
 fingers = [1 if lmList[tipId][1] > lmList[tipId - 1][1] else 0 for tipId in
tipIds]
 total = fingers.count(1)
 led(total)
# DISPLAY FINGER COUNT AND LED STATUS ON THE FRAME
 cv2.putText(image, str(total), (45, 375),
cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
 cv2.putText(image, "Led", (100, 375),
cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

THE END OF CODE
 # DISPLAY THE FRAME
 cv2.imshow("Frame", image)
 # CHECK FOR KEY PRESS TO EXIT THE LOOP
 k = cv2.waitKey(1)
 if k == ord('q'):
 break
# RELEASE VIDEO CAPTURE AND CLOSE WINDOWS
 video.release()
 cv2.destroyAllWindows()
