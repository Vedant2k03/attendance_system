import cv2
import time

webcam_index = 0
#rtsp_url = 'rtsp://<username>:<password>@<ip_address>:<port>/stream'

capture_duration = 10  
output_file = 'captured_video.mp4'


cap = cv2.VideoCapture(webcam_index)

if not cap.isOpened():
    print("Error: Unable to open webcam feed.")
    exit()


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

start_time = time.time()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame is successfully read
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Write the frame to the output video file
    out.write(frame)

  
    cv2.imshow('Live Feed', frame)

    # Check for key press to end the live stream capture
    key = cv2.waitKey(1)
    if key == ord('q'):  # Quit the program
        break
        # Check for key press to start/stop the live stream capture
    #key = cv2.waitKey(1)
    #if key == ord('s'):  
       # if not stream_running:
            #start_time = time.time()
            
            #stream_running = True
            #print("Live stream capture started.")
    #elif key == ord('e'):  
        #if stream_running:
            #stream_running = False
            #print("Live stream capture ended.")
    #elif key == ord('q'):  
       # break
 
    if time.time() - start_time >= capture_duration:
        print("Live stream capture ended due to specified duration.")
        break


cap.release()
out.release()
cv2.destroyAllWindows()

import cv2

def capture_and_analyze(video_path, output_folder, target_fps):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the actual frames per second of the video
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Actual frames per second: {actual_fps}")

    # Calculate the frame interval based on the target_fps
    frame_interval = int(actual_fps / target_fps)

    # Loop through frames with the specified interval
    frame_number = 0
    while True:
        # Read the next frame
        ret, frame = cap.read()

        # Break the loop if the video has ended
        if not ret:
            break

        # Save the frame as an image
        output_image_path = f"{output_folder}/frame_{frame_number}.jpg"
        cv2.imwrite(output_image_path, frame)

        # Perform analysis (replace this with your actual analysis code)
        #analyze_frame(frame)
        

        # Increment frame number
        frame_number += 1

        # Skip frames based on the calculated frame interval
        for _ in range(frame_interval - 1):
            cap.read()

    # Release the video capture object
    cap.release()



if __name__ == "__main__":
    # Specify the path to your video file
    video_path = output_file


    # Specify the output folder for the captured frames
    output_folder = "output_frames4"

    # Specify the desired frames per second for output
    target_fps = 1

    # Create the output folder if it doesn't exist
    import os
    os.makedirs(output_folder, exist_ok=True)

    # Call the function to capture and analyze frames
    capture_and_analyze(video_path, output_folder, target_fps)