from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np
import time

class Button:
    def __init__(self,pos,width,height,value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (225, 225, 225), cv2.FILLED)  # This is the shape of the calculator
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)  # This is the shape of the calculator
        cv2.putText(img, self.value, (self.pos[0]+ 40, self.pos[1] + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False




################ Creating Buttons ###################
buttonValues = [["7","8","9","*"],
                ["4","5","6","-"],
                ["1","2","3","+"],
                ["0","/",".","="]]
buttonList = list()
for i in range(4):
    for j in range(4):
        xpos = i*100 + 700
        ypos = j*100 + 150
        buttonList.append(Button((xpos,ypos),100,100, buttonValues[j][i]))

### Variables ###
myEquation = ""
delayCounter = 0

###############   Webcam     ####################
cap= cv2.VideoCapture(0)
cap.set(3,1280) # we increase the width of the camera frame prop id 3 reprsents width
cap.set(4,980) # we increase height of the image, prop id 4 represents height

detector = HandDetector(detectionCon=0.8, maxHands=1) # we want just a single hand with maxHands parameter

while True:
    success, img = cap.read()# Get frame from webcam
    img = cv2.resize(img, (1280, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    img = cv2.flip(img,1) # 1 will flip horzontally 0 vertically

    # Detect hand and its location
    hands, img = detector.findHands(img, flipType=False)

    ## draw all buttons ##
    cv2.rectangle(img, (700,70), (700+ 400, 70 + 100),
                  (225, 225, 225), cv2.FILLED)  # This is the shape of the calculator
    cv2.rectangle(img, (700, 70), (700 + 400, 70 + 100),
                  (50, 50, 50), 3)  # This is the shape of the calculator


    for button in buttonList:
        button.draw(img)

    ## Processing ##
    #Check for Hand#
    if hands:
        # Find distance between fingers
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)

        x, y = lmList[8]
        print(length)
        if length < 100:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = buttonValues[int(i % 4)][int(i / 4)]  # get correct number
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

            # to avoid multiple clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0
    ## Display Result ##
    cv2.putText(img, myEquation, (710, 130),
                cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    ##Display Image ##
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''



#img = cv2.resize(img, (1280, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)



