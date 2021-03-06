import tensorflow.keras
import numpy as np
import cv2
from process_labels import gen_labels
from roastScript import roast
import keyboard
from swiper import swipeLeft
from swiper import swipRight
from flirtTalk import flirt
from roastScript import roast
from roastScript2 import roast1
from flirtTalk2 import flirt1

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
image = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

#image = cv2.VideoCapture(0)
i=0
e=0
q = 0
# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

"""
Create the array of the right shape to feed into the keras model
The 'length' or number of images you can put into the array is
determined by the first position in the shape tuple, in this case 1."""
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# A dict that stores the labels
labels = gen_labels()

while True:
    # Choose a suitable font
    font = cv2.FONT_HERSHEY_SIMPLEX
    ret, frame = image.read()
    frame = cv2.flip(frame, 1)
    # In case the image is not read properly
    if not ret:
        continue
    # Draw a rectangle, in the frame
    frame = cv2.rectangle(frame, (220, 80), (530, 360), (0, 0, 255), 3)
    # Draw another rectangle in which the image to labelled is to be shown.
    frame2 = frame[80:360, 220:530]
    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    frame2 = cv2.resize(frame2, (224, 224))
    # turn the image into a numpy array
    image_array = np.asarray(frame2)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    pred = model.predict(data)
    result = np.argmax(pred[0])

    # Print the predicted label into the screen.
    cv2.putText(frame,  "check : " +
                labels[str(result)], (280, 400), font, 1, (0, 255, 0), 2, cv2.LINE_AA)


    # Exit, when 'q' is pressed on the keyboard
    if cv2.waitKey(1) and 0xff == ord('q'):
        exit = True
        break
    # Show the frame   
    cv2.imshow('Frame', frame)
    if(keyboard.is_pressed('f')):
        print("f in the chat")
        e = 0
        i = 1
        print(i)
    if(labels[str(result)] == "Hot" and i ==1):
        if(e < 35):
            e += 1
            print(e)
        if(e == 35 and i ==1):
            print("flirting")
            if(q <=20):
                flirt()
            if(q>20):
                flirt1()           
            swipRight()
            print("flirt")
            i += 1
            q += 1
            print(q)
    if(labels[str(result)] == "Not" and i ==1):
        if(e < 35):
            e += 1
            print(e)
        if(e == 35 and i ==1):
            print("roasting")
            if(q <=20):
               roast()
            if(q>20):
                roast1()
            swipeLeft()
            print("roast")
            i += 1
            q += 1
            print(q)
image.release()
cv2.destroyAllWindows()
