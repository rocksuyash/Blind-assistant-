import argparse
import os
import time
import urllib.request

from gtts import gTTS

from methods import *

parser = argparse.ArgumentParser()
parser.add_argument('--webcam', type=bool, default=True)
parser.add_argument('--url', type=str, default='http://192.168.0.4:8080/shot.jpg')

args = parser.parse_args()
KNOWN_DISTANCE = 30.0
KNOWN_WIDTH = 3
url = args.url
if args.webcam:
    cap = cv2.VideoCapture(0)
    _, c_image = cap.read()
else:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    c_image = cv2.imdecode(imgNp, -1)
marker = find_marker(c_image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
time.sleep(2)
print("Main program Staring")
while True:
    if args.webcam:
        _, image = cap.read()
    else:
        imgResp = urllib.request.urlopen(url)
        image = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    marker = find_marker(image)
    CM = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    print("%.2fcm" % CM)
    cv2.putText(image, "%.2fcm" % CM,
                (image.shape[1] - 350, image.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (255, 0, 0), 3)
    cv2.imshow("image", image)
    myText = ("%.2fcm" % CM)
    language = 'en'
    output = gTTS(text=myText, lang=language, slow=False)
    output.save("output.mp3")
    os.system("start output.mp3")
    time.sleep(4)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
