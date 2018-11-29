import cv2


pic_num=22
img = cv2.imread("kn.jpg")
# should be larger than samples / pos pic (so we can place our image on it)
resized_image = cv2.resize(img, (250, 50))
cv2.imwrite("negi/"+str(pic_num)+".jpg",resized_image)
