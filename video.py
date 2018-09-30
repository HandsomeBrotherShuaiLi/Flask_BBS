from statistics import mode
import cv2
from keras.models import load_model
from h5py import *
import numpy as np
def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x
def draw_bounding_box(face_coordinates, image_array, color):
    x, y, w, h = face_coordinates
    cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)
def draw_text(coordinates, image_array, text, color, x_offset=0, y_offset=0,
                                                font_scale=2, thickness=2):
    x, y = coordinates[:2]
    cv2.putText(image_array, text, (x + x_offset, y + y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA)

def detection(path1,path2):
emotion_labels={0:'angry',1:'disgust',2:'fear',3:'happy',4:'sad',5:'surprise',6:'neutral'}
gender_labels={0:'woman',1:'man'}
font=cv2.FONT_HERSHEY_SIMPLEX

frame_window=10
emotion_offsets=(20,40)
gender_offsets=(30,60)
#loading models

while True:
    bgr_image=video_capture.read()[1]
    gray_image=cv2.cvtColor(bgr_image,cv2.COLOR_BGR2GRAY)
    rgb_image=cv2.cvtColor(bgr_image,cv2.COLOR_BGR2RGB)

    faces=detection_model.detectMultiScale(gray_image,1.3,5)

    for face_coordinates in faces:
        x,y,w,h=face_coordinates
        x0,y0=emotion_offsets
        x3,y3=gender_offsets
        x1=x-x0
        x2=x+w+x0
        y1=y-y0
        y2=y+h+y0
        gray_face=gray_image[y1:y2,x1:x2]
        x1=x-x3
        x2=x+w+x3
        y1=y-y3
        y2=y+h+y3
        rgb_face=rgb_image[y1:y2,x1:x2]
        try:
            gray_face=cv2.resize(gray_face,(emotion_target_size))
            rgb_face=cv2.resize(rgb_face,(gender_target_size))
        except:
            continue
        gray_face=preprocess_input(gray_face,False)
        gray_face= np.expand_dims(gray_face,0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text=emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        rgb_face = np.expand_dims(rgb_face, 0)
        rgb_face = preprocess_input(rgb_face, False)
        gender_prediction = gender_classifier.predict(rgb_face)
        gender_label_arg = np.argmax(gender_prediction)
        gender_text = gender_labels[gender_label_arg]
        gender_window.append(gender_text)

        if(len(emotion_window)>frame_window or len(gender_window)>frame_window):
            emotion_window.pop(0)
            gender_window.pop(0)
        try:
            emotion_mode=mode(emotion_window)
            gender_mode=mode(gender_window)
        except:
            continue
        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0))
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
        else:
            color = emotion_probability * np.asarray((0, 255, 0))

        if gender_text == 'woman':
            color2=(255,0,0)
        else:
            color2=(0,255,0)

        color = color.astype(int)
        color = color.tolist()
        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_mode,
                  color, 0, -45, 1, 1)
        #去掉下面的注释就会显示性别的识别结果
        # draw_text(face_coordinates, rgb_image,gender_mode,color2,0,-20,1,1)
    bgr_image=cv2.cvtColor(rgb_image,cv2.COLOR_RGB2BGR)
    cv2.imshow('facial emotion & gender analysis',bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





