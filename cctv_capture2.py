import cv2
import time

# RTSP URLs of the CCTV cameras
#rtsp_url_1 = 'rtsp://<username>:<password>@<ip_address_1>:<port_1>/stream'
#rtsp_url_2 = 'rtsp://<username>:<password>@<ip_address_2>:<port_2>/stream'
webcam_index1=0
webcam_index2=1
capture_duration = 10  


output_file_1 = 'captured_video_1.mp4'
output_file_2 = 'captured_video_2.mp4'

cap_1 = cv2.VideoCapture(webcam_index1)
cap_2 = cv2.VideoCapture(webcam_index2)


if not cap_1.isOpened():
    print("Error: Unable to open camera 1 feed.")
    exit()

if not cap_2.isOpened():
    print("Error: Unable to open camera 2 feed.")
    exit()


frame_width = int(cap_1.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap_1.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_1 = cv2.VideoWriter(output_file_1, fourcc, 20.0, (frame_width, frame_height))
out_2 = cv2.VideoWriter(output_file_2, fourcc, 20.0, (frame_width, frame_height))


start_time = time.time()

while True:
   
    ret_1, frame_1 = cap_1.read()
    ret_2, frame_2 = cap_2.read()

 
    if not ret_1 or not ret_2:
        print("Error: Unable to read frames from one or both cameras.")
        break


    out_1.write(frame_1)
    out_2.write(frame_2)
    cv2.imshow('Live Feed 1', frame_1)
    cv2.imshow('Live Feed 2', frame_2)

    key = cv2.waitKey(1)
    if key == ord('q'):  
        break
    if time.time() - start_time >= capture_duration:
        print("Live stream capture ended due to specified duration.")
        break
cap_1.release()
cap_2.release()
out_1.release()
out_2.release()
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
    video_path_1 = output_file_1 
    video_path_2 = output_file_2 

    # Specify the output folder for the captured frames
    output_folder_1 = "output_frames4_1"
    output_folder_2 = "output_frames4_2"
    # Specify the desired frames per second for output
    target_fps = 1

    # Create the output folder if it doesn't exist
    import os
    os.makedirs(output_folder_1, exist_ok=True)
    os.makedirs(output_folder_2, exist_ok=True)
    # Call the function to capture and analyze frames
    capture_and_analyze(video_path_1, output_folder_1, target_fps)
    capture_and_analyze(video_path_2, output_folder_2, target_fps)