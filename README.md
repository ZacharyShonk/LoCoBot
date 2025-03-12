# LoCoBot
A project to get LoCoBot running in 2025 via modified scripts and setup.

## Setup
In this repository there is a "setup.py" and "KobukiSetup.sh" file. Both of these files will help with setting up the robot.

### Step 1:
  If you are using a standard _LoCobot_ with a camera, the kobuki, and the mini computer make sure that you have ubuntu 20.0.4 installed on the computer and setup SSH.
  Refer to [Ubuntu SSH Documentation](https://documentation.ubuntu.com/server/how-to/security/openssh-server/index.html) for the setup process. On your main computer use "Visual Studio Code" and the Microsoft Remote Development extension to remotely connect to your robot.   From here you want to move onto Step 2.
### Step 2:
  Install the files (run.txt, setup.py, pykobuki.cpp, KobukiSetup.sh, coco.names, and robot_example.py) from our repo. These files will allow you to interact with the robot, and code your own actions for it. Now that they are installed pull them into a folder in
  Visual Studio Code so they replicate to your robot.
### Step 3:
  Run the KobukiSetup.sh file in the robots terminal and let it do its work. Once the KobukiSetup.sh file is done run the setup.py file using the command "sudo python3 setup.py build" and once that is done run the command "sudo python3 setup.pe install" these two commands
  will set up the pykobuki wrapper that we made so people can code in Python on the robot.
### Step 4:
  Test the robot_example.py file to make sure the robot works, this file is a demo made we made that uses object detection to avoid objects. You can also use this file to self drive the robot. 
  The controls for self drive are:
    W - Forward
    A - Turn Left
    S - Backwards
    D - Turn Right
  If everything is working and there arent errors then you can make your own Python file and make your own robot actions.
