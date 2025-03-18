# Step 1: Prepare the System
The setup has been tested on **Ubuntu 20.04**, but other Linux distributions may work as well. Ensure that:
- Your system meets the hardware requirements.
- SSH is set up for remote access.

Refer to the [Ubuntu SSH Documentation](https://documentation.ubuntu.com/server/how-to/security/openssh-server/index.html) for SSH setup instructions.  
On your main computer, use **Visual Studio Code** with the **Microsoft Remote Development** extension to remotely connect to your robot.  
Once connected, proceed to Step 2.

# Step 2: Install and Run Setup Scripts
Run the following files from this repository in order:

1. **Run `KobukiSetup.sh`** to set up system dependencies:
   ```bash
   bash KobukiSetup.sh
   ```
2. **Run `setup.py`** to install the **pykobuki** wrapper, enabling Python-based control of the robot:
   ```bash
   sudo python3 setup.py build
   sudo python3 setup.py install
   ```
