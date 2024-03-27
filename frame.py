import os
import cv2
from retinaface import RetinaFace

# Path to the folder containing frames
folder_path = "output_frames_1"

# Initialize RetinaFace
detector = RetinaFace

# Initialize variables to keep track of the best frame and number of faces
best_frame = None
max_faces = 0

# Iterate through each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):
        image_path = os.path.join(folder_path, filename)
        frame = cv2.imread(image_path)

        # Detect faces in the frame
        faces = detector.detect_faces(frame)
        num_faces = len(faces)

        # Update best frame if needed
        if num_faces > max_faces:
            max_faces = num_faces
            best_frame = frame

# Do something with the best frame, e.g., save it to disk
cv2.imwrite("best_frame_with_faces.jpg", best_frame)

detected_faces = detector.extract_faces(best_frame)
# detected_faces = detector.extract_faces("test.jpg")

# Define the desired size for the output images
desired_size = (224, 224)

# Iterate over the list of images and resize each one
images = [cv2.resize(image, desired_size) for image in detected_faces]


import pandas as pd
from deepface import DeepFace
import xlwings as xw
import datetime

# xlwings
workbook=xw.Book('attendance.xlsx')
sheet_name=datetime.date.today().isoformat()
try:
    worksheet=workbook.sheets(sheet_name)
except:
    worksheet=workbook.sheets.add(sheet_name)
    
worksheet.range('A1').value = 'STUDENT_REG'
worksheet.range('B1').value = 'DATE '
worksheet.range('C1').value = 'TIME'
worksheet.range('D1').value = 'CLASS'
worksheet.range('E1').value = 'DIVISION'
worksheet.range('F1').value = 'NAME'
students = []
s = 2
student_info_df = pd.read_csv('data.csv')

# Display the DataFrame
print(student_info_df)

# Get today's day
t0 = datetime.date.today().day

# Function to get student details by registration number
def get_student_details(registration_number):
    print("Searching for registration number:", registration_number)
    # Convert registration_number to integer
    registration_number = int(registration_number)
    
    # Check the data type of the 'Registration No' column
    print("Data type of 'Registration No' column:", student_info_df['Registration No'].dtype)
    # Check the data type of the registration_number variable
    print("Data type of registration_number variable:", type(registration_number))
    student_details = student_info_df[student_info_df['Registration No'] == registration_number]
    print("Found student details:", student_details)
    if not student_details.empty:
        return student_details.iloc[0]  # Assuming registration number is unique, return first match
    else:
        return None

# Loop until running is False
for test_image in images:
    moment = datetime.datetime.now()
    hour = moment.hour
    minute = moment.minute
    day = moment.day
    month = moment.month
    year = moment.year

    date = f"{day}-{month}-{year}"
    time = f"{hour}:{minute}"

# Check if day has changed
if day != t0:
    t0 = day
    worksheet = workbook.sheets.add(date)
    worksheet.range('A1').value = 'STUDENT_REG'
    worksheet.range('B1').value = 'DATE '
    worksheet.range('C1').value = 'TIME'
    worksheet.range('D1').value = 'class_name'
    worksheet.range('E1').value = 'DIVISION'
    worksheet.range('F1').value = 'NAME'
    students = []
    s = 2

# Predict identity using DeepFace for the current test image
model = DeepFace.find(img_path=test_image, db_path='./database', enforce_detection=False, model_name='VGG-Face')
if len(model) > 0 and 'identity' in model[0]:
    predicted_reg_no = model[0]['identity'][0].split('/')[1].split('\\')[1]  # Assuming identity corresponds to registration number
    print("Predicted Registration Number:", predicted_reg_no)  # Print the predicted registration number

    # Get student details using predicted registration number
    student_details = get_student_details(predicted_reg_no)
    print("lets see students details nowwwwww")
    print(student_details)

if student_details is not None:
    student_name = student_details['Name']
    print(student_name)
    student_class = student_details['class_name']
    print(student_class)
    student_division = student_details['Div']
    print(student_division)

# Insert predicted name, class, and division into Excel sheet
if predicted_reg_no not in students:
    worksheet.range(f'A{s}').value = predicted_reg_no
    worksheet.range(f'B{s}').value = date
    worksheet.range(f'C{s}').value = time
    worksheet.range(f'D{s}').value = student_class
    worksheet.range(f'E{s}').value = student_division
    worksheet.range(f'F{s}').value = student_name
    students.append(predicted_reg_no)
    s += 1
