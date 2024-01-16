import cv2
import numpy as np
import time

# Define lower and upper bounds of red dot
redLower = (0, 95, 42)
redUpper = (171, 255, 255)

# Define ROI coordinates
rect_x_offset = int((600 - 320) / 2)
rect_y_offset = int((450 - 240) / 2)
rect_topleft = (rect_x_offset, rect_y_offset)
rect_bottomright = (rect_x_offset + 320, rect_y_offset + 240)

if __name__ == '__main__':
    # Initialize video capture
    vs = cv2.VideoCapture(0)

    # Allow webcam to warm up
    time.sleep(2.0)

    while True:
        # Read a frame from the webcam
        _, frame = vs.read()

        if frame is None:
            break

        # Resize frame for faster processing
        frame = cv2.resize(frame, (600, 450))

        # Convert frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask for red color
        mask_red = cv2.inRange(hsv, redLower, redUpper)

        # Draw blue bounding box for ROI
        cv2.rectangle(frame, pt1=rect_topleft, pt2=rect_bottomright, color=(255, 0, 0), thickness=2)

        # Create border to mask out regions outside the ROI
        border = np.zeros((450, 600), dtype="uint8")
        cv2.rectangle(border, rect_topleft, rect_bottomright, 255, thickness=-1)

        # Apply border mask to red mask
        result_red = cv2.bitwise_and(mask_red, mask_red, mask=border)

        # Find contours for red laser dot
        cnts_red, _ = cv2.findContours(result_red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Variables to store center coordinates
        center_red = None

        # Process the red laser dot
        if len(cnts_red) > 0:
            # Find the largest contour for the red laser dot
            c_red = max(cnts_red, key=cv2.contourArea)

            # Calculate the minimum enclosing circle and its centroid
            ((x_red, y_red), radius_red) = cv2.minEnclosingCircle(c_red)
            M_red = cv2.moments(c_red)

            # Check if the contour is large enough and within the ROI
            if M_red["m00"] != 0 and radius_red > 3 and x_red >= rect_x_offset and x_red <= rect_x_offset + 320 and y_red >= rect_y_offset and y_red <= rect_y_offset + 240:
                center_red = (int(x_red), int(y_red))

                # Draw a rectangle around the red dot
                x, y, w, h = cv2.boundingRect(c_red)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Display the frame
        cv2.imshow("Frame", frame)

        # Check for ESC key press
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    # Close the webcam
    vs.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

