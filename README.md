# BigBro

Objective:
This project is aimed at home safety and car safety, specifically against intrusion, breaking and entering, and theft issues.


Description:
The main idea is to monitor the inside of the structure, detect the presence of a person via face detection, and if a person is detected an image capture is sent to the AWS server. Once the image is received, there is a file creation trigger that triggers an AWS Lambda function. The Lambda function then reads in the newly added image, compares it with the family images, and if no match is found it sends out an email with a website link where the website displays the captured image and creates an intruder alert. Otherwise, a match is found, and no alert will be created. The idea can be extended to monitoring both the outside and the inside of the house, and the inside of a vehicle, where the system can be turned on and off at the owner's will to accomodate for privacy.


Directory Structure:
- AWS (server side directory)
	- lambda (lambda functions that contain triggers linked to s3 bucket upload) (Python 3.6)
		- E-mail-Face-Recognition
			-lambda_function.py
	- images (stored on the s3 bucket 'hackarizonaasu')
		- all family members images...
		- suspect.jpg
		- intruder.jpg
- Capture (local directory) (Python 3.8)
	- capture.py
	- haarcascade_frontalface_default.xml
	- suspect.jpg (this file is created when a person is detected in the live feed and sent to the AWS server)


Dependencies:
- Local side
	- cv2
	- boto
