# smart-security-system

The Smart Security System is an IoT device that uses a Raspberry Pi, camera, and PIR motion sensor to detect movement and identify faces. When motion is detected, the camera takes a photo. The system uses Python, OpenCV, and the face_recognition library to compare the captured face to a database of authorised users. If an unknown face is detected, the system sends an instant alert with the photo to Telegram for remote security monitoring.
