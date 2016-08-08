# Autonomous Monitoring System (AMS)

This system allows you to monitors all the activities in a place using a camera and a Python software running on a single-board computer.

## Motivations

When far from home, it is sometimes useful (if not necessary) to be aware of what is going on there, whether it be to check if the kids are safe, if the domestic robot has finished its current chore, if no one has broken in, or to acquire and keep traces of a burglary.
The AMS was designed to provide an easily-installed solution to this problem.

## Main features

* Automatic detection of movement and selection of interesting frames
* Upload of the selected frames to a cloud service (such as Dropbox)
* Access to an online web page through a VPN, allowing to:
  * visualize the last uploaded frames
  * visualize a real-time video live stream 
  * configure several parameters related to the detection and the upload
  * look over the log files
* Handling of hardware and software problems, including backup of the frames in case of internet connection break down, with regular new attempts to connect

## Hardware

This project uses the Raspberry Pi 3 as the single-board computer and processing unit. Its quadcore feature allows to paralillize the whole process and thus maximize the performances — mainly frame rate and server responsiveness.
Any USB webcam or camera can be used as the capturing device. A wide angle lens is a plus if image distortion is not critical.

## Software

The main application is written in Python and is composed of four modules running in parallel using the `multiprocessing` library.

* Capture: it takes care of the image capture process. For a maxmium efficiency, it directly deals with the Video4Linux2 drivers through a ligth and low-level Python API called `python-v4l2capture`.
* Processing: it processes the frames and detects movements using the OpenCV library.
* Cloud: it sends the selected frames to a Dropbox folder and sends email alerts in case of failure.
* Server: it handles client requests to web pages using the Bottle back-end web-framework and the Rocket WSGI. Pages are rendered using the Bootstrap front-end framework (with HTML and CSS).

## Setup

Before running the application, make sure you have installed:
* Python 2.7
* OpenCV 3.0 for Python ([this guide](http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/) can help)
* the folowing Python packages: `bottle`, `rocket`, `requests`, `dropbox` and `v4l2capture` ([v1.5 from GitHub](https://github.com/gebart/python-v4l2capture))

You should also modify the configuration file `conf.json` which contains your Dropbox account settings. The token and keys are accessible from your [application page](https://www.dropbox.com/developers/apps) after creating a new App.

The web page is rendered on `localhost:8000`. To access it from the Internet (i.e. outside your local network), you need to use a VPN service, such as [Weaved](https://www.weaved.com/) (which also allows you to remotely debug/update the device via SSH or VNC).

## Incoming features
* Email alerts in case of camera failure
* Visualization of a real-time video live stream through the online web page

## Credits

The whole application was designed and written by Paul-Edouard Sarlin. It was inspired by a [post](http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/) from Adrian Rosebrock on his [PyImageSearch](http://www.pyimagesearch.com/) blog.


