import os
import time

import cv2
from PIL import Image
from gtts import gTTS
from pytesseract import pytesseract

camera = cv2.VideoCapture(0)
while True:
    _, image = camera.read()
    cv2.imshow("Text detection", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('test1.jpg', image)
        break
camera.release()
cv2.destroyAllWindows()


def tesseract():
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract"
    Imagepath = "test1.jpg"
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(Image.open(Imagepath))

    myText = text[:-1]

    language = 'en'

    output = gTTS(text=myText, lang=language, slow=False)

    output.save("output.mp3")

    os.system("start output.mp3")
    time.sleep(1)


tesseract()
