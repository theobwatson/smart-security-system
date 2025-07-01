
import cv2
import face_recognition
import os
import time
import RPi.GPIO as GPIO
import telegram_send
import subprocess

# setup GPIO for PIR sensor
PIR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# load known faces
known_encodings = []
known_names = []
known_faces_folder = '/home/pi/smart_security/known_faces'

for filename in os.listdir(known_faces_folder):
    img = face_recognition.load_image_file(os.path.join(known_faces_folder, filename))
    encodings = face_recognition.face_encodings(img)
    if encodings:
        known_encodings.append(encodings[0])
        known_names.append(os.path.splitext(filename)[0])
        
print("number of known encodings loaded: ", len(known_encodings))
print("known names:", known_names)
        
def send_telegram(img_path):
    subprocess.run(["telegram-send", "--image", img_path, "--caption", "Unknown face detected!"])
    
def capture_with_libcamera(output_path):
    subprocess.run(["libcamera-still", "-o", output_path, "--nopreview", "-t", "1000"])
    
print("System ready. Waiting for motion")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected")
            img_path="/home/pi/smart_security/captured.jpg"
            capture_with_libcamera(img_path)
            
            # recognise faces
            unknown_img = face_recognition.load_image_file(img_path)
            face_locations = face_recognition.face_locations(unknown_img)
            unknown_encodings = face_recognition.face_encodings(unknown_img, face_locations)
            
            detected = False
            
            for idx, unknown_encoding in enumerate(unknown_encodings):
                distances = face_recognition.face_distance(known_encodings, unknown_encoding)
                print("Face distances: ", distances)
                results = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=0.7)
                print("Matching results: ", results)
                if True in results:
                    print("Authorised face detected")
                    detected = True
                    break
            
                
            if not detected and unknown_encodings:
                print("Unknown face. Sending Telegram alert.")
                send_telegram(img_path)
            elif not unknown_encodings:
                print("No face detected")
                
            time.sleep(5)
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
