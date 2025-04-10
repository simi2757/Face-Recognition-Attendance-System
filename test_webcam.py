import cv2


def test_webcam():
    # Try to open the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Webcam opened successfully")
    
    # Try to read a frame
    ret, frame = cap.read()
    if ret:
        print("Successfully read frame from webcam")
        # Display the frame
        cv2.imshow('Test Frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Could not read frame from webcam")
    
    # Release the webcam
    cap.release()

if __name__ == "__main__":
    test_webcam() 