import cv2
import oj

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_trainer/trainer.yml')
cascadePath = r'C:/Users/0ng/Anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

idnum = 0

names = ['0ng']
msg = {
    "0ng": {
        "id": "2018104021",
        "pwd": "123456"
    },
}
nums = {
    "0ng": 0,
    "unknown": 0,
}
# cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# while True:
for case in range(100):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH))
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        idnum, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 100:
            idnum = names[idnum]
            confidence = "{0}%".format(round(100 - confidence))
        else:
            idnum = "unknown"
            confidence = "{0}%".format(round(100 - confidence))

        nums[str(idnum)] += 1
        cv2.putText(img, str(idnum), (x+5, y-5), font, 1, (0, 0, 255), 3)
        cv2.putText(img, str(confidence), (x+5, y+h-5), font, 1, (0, 0, 0), 3)

    cv2.imshow('camera', img)
    k = cv2.waitKey(10)
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()
num = 0
usr = None
for k, v in nums.items():
    if v > num:
        num = v
        usr = k
if usr != "error":
    print("user:", usr)
    oj.login(msg[usr])
else:
    print("No user!")
