# webcam-sentry

Webcam sentry is a web app that allows you to monitor your room when you are not around, all you need is a browser and a webcam!

## How it works
Webcam sentry will allow you to whitelist people you trust to be in your room, however, if any else tries to enter the sentry will notify you using an email

## Tech stack
Frontend:
  1. Bootstrap
  2. jQuery
  3. JavaScript
  
Backend:
  1. Flask (Python)
  2. SQLite3
  3. Dlib (For face recognition)

Development environement: Ubuntu Linux (16.04)

The webcam.js module used for this project was adopted from https://github.com/jhuckaby/webcamjs
Face recognition is done using the following library https://github.com/ageitgey/face_recognition since it is so great and accurate
