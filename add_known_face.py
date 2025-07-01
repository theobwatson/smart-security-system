import subprocess
import time
import os
import face_recognition

known_faces_dir = "/home/pi/smart_security/known_faces"

def take_photo(temp_path):
    # take a photo and save to temp path
    subprocess.run(["libcamera-still", "-o", temp_path, "--nopreview", "-t", "1000"])
    
def face_found_in_photo(img_path):
    img = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(img)
    return len(encodings) > 0

# ask user for name to save the photo as
name = input("Enter a name for this face: ").strip()

if name == "":
    print("No name entered, exiting.")
    exit(1)
    
output_path = os.path.join(known_faces_dir, f"{name}.jpg")
temp_path = "/home/pi/smart_security/temp_face.jpg"

while True:
    input("Press enter to take a photo...")
    take_photo(temp_path)
    
    print("Checking photo for a face...")
    
    if face_found_in_photo(temp_path):
        os.rename(temp_path, output_path)
        print(f"Face detected. Photo saved as {output_path}")
        break
    else:
        print("No face detected. Please try again.")
        time.sleep(1)
