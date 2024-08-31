import cv2

def capture_image(output_file):
    # Open a connection to the camera (0 is usually the first camera)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    # Set the camera resolution to 300x300
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

    # Read a frame from the camera
    ret, frame = camera.read()

    if not ret:
        print("Error: Could not read from camera.")
        return

    # Save the captured image
    cv2.imwrite(output_file, frame)
    print(f"Image captured and saved as {output_file}")

    # Release the camera
    camera.release()

if __name__ == "__main__":
    output_filename = "captured_image.jpg"
    capture_image(output_filename)
