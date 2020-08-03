import os
from flask import Flask, render_template

app = Flask(__name__)

# What are we running on?
isRPi = False
if os.uname()[4][:3] == 'arm':
    import automationhat  # pylint: disable=all
    isRPi = True


# Our default homepage
@app.route('/')
def index():
    return render_template('index.html')


# Grab a still from the camera
@app.route('/photo')
def photo():
    return render_template('photo.html')


# Stream video from the camera
@app.route('/video')
def video():
    return render_template('video.html')


# Show previous video
@app.route('/history')
def history():
    return render_template('history.html')


# Start the web server on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0')
