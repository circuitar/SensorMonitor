SensorMonitor
=============

This is a project for a web-based sensor monitor using Arduino and/or the [Nanoshields](http://www.circuitar.com.br/nanoshields).

It collects data from sensors and sends it to a server in the local network using an Ethernet Nanoshield (or a regular Arduino Ethernet Shield with the W5100 chip).

This data is stored in a database on the server and is shown, in real time, on a set of gauges when you access a web page. The web server runs in Python, using the Django framework.

## Installation Instructions

These are installation instructions for a simple setup of a web server in your local machine. To create a robust installation, please check the "WARNING" section below.

1. Install Python 2.7
    1. On Windows, download and install [this](http://python.org/ftp/python/2.7.6/python-2.7.6.msi)
    1. On Mac OSX, follow [these instructions](http://docs.python-guide.org/en/latest/starting/install/osx/)
    1. On Linux, follow [these instructions](http://docs.python-guide.org/en/latest/starting/install/linux/)
1. Install `pip`
    1. On Windows:
        1. Download and install `setuptools` for Python 2.7 from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools)
        1. Download and install `pip` from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip)
        1. Add `C:\Python27` and `C:\Python27\Scripts` to your PATH environment variable:
            1. Click Start, start typing "Edit the system environment variables" and open it
            1. Click "Environment Variables..."
            1. In "System Variables", select "PATH" and click "Edit..."
            1. At the end of "Variable value:", add `;C:\Python27\Scripts` and click OK three times
    1. On Linux or on Mac OSX, you can find the instructions Python installation links above
1. Install Django 1.6
    1. On Windows:
        1. Open an administrator command prompt by right-clicking in "Command Prompt" and selecting "Run as Administrator"
        1. Run `pip install Django`
    1. On Linux of Mac OSX:
        1. Open the terminal and run `sudo pip install Django`
1. Download the ZIP with all the source code or clone this GIT repository
1. Open a command prompt and go to the directory where this README file is, and where manage.py resides
1. Run `python manage.py syncdb`
    1. When asked to create a superuser, answer "yes"
    1. Select a username, e-mail and password of your choice
1. Find the IP address of your computer in the local network running `ipconfig` in Windows or `ifconfig` in Mac or Linux
    1. For the instructions below, we will assume your IP is `192.168.0.10`, so please replace it as needed
1. Run `python manage.py runserver 192.168.0.10:8000`
    1. On Windows, if a dialog shows up asking for permissions, select "Allow access"
    1. If needed, allow access to port 8000 in your firewall by adding a rule (or disable the firewall for a quick test, but it's not recommended)
1. Open you browser at http://192.168.0.10:8000/admin, and log in using the username and password you created above
1. Add the sensors you need, one for each gauge:
    1. Click in Sensor Types and then Add Sensor Type
    1. Choose a name: this will show up on top of each gauge
    1. Choose a code: this will be used in the Arduino code to send data to this gauge
        1. To make things simple, use only lower case letters, numbers and underscores, e.g. `temp1` or `ext_temp`
    1. Choose the maximum and minimum values that are adequate for your sensor
    1. Choose the sensor units (e.g. "volts", "degrees", etc.): this will be shown right below the gauge value
    1. Click "Save" and repeat for each sensor you want to add
1. Modify the `BasicSensorMonitor` example in the `arduino` folder to match the sensors you have:
    1. All you have to do is to populate correctly the string that is sent to the server
    1. The main line of code that needs to be changed is: `sprintf(params, "voltage1=%d.%02d&voltage2=%d.%02d", DECIMAL(v1, 2), DECIMAL(v2, 2));`
    1. Replace `voltage1`, `voltage2`, etc. with the sensor codes you created above
    1. Replace the variables `v1` and `v2` with the variables that contain the sensor data in your Arduino code
    1. Adjust the number of decimal places as you need it
    1. Add more sensors if you need
    1. Don't forget to increase the `params[]` string size to accommodate your data!
1. Upload the Arduino code
1. Open you browser at http://192.168.0.10:8000/admin and enjoy!

### WARNING

This is a sample application and is not suitable for a production environment. It offers no authentication or other security mechanisms. If you wish to run it in a secure production environment, here are some recommendations:

- Run it on a physically isolated network if you just need a local application
- Use a proper production deployment for Django instead of the development web server outlined here (there are lots of tutorial for that on the web)
- If you are running it remotely over the web, do so through a secure VPN
- Take care of database size, and create some job to delete old sensor data
- Create proper firewall rules in your server
- This code is provided free of charge, so run it at your own risk!

---

Copyright (c) 2013 Circuitar

This software is released under an MIT license. See the attached LICENSE file for details.
