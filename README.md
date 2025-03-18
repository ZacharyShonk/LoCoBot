# **LoCoBot**

*A project to run LoCoBot in 2025 using pure Python with minimal C++.*

## **Table of Contents**

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Documentation](#documentation)
5. [License](#license)

---

## **Overview**

LoCoBot is designed to operate using pure Python with minimal C++ integration, aiming for ease of use and flexibility in robotic applications.

---

## **Installation**

For detailed installation instructions, please refer to the [install.md](docs/install.md) file. This document includes system requirements, dependency installations, and setup procedures.

---

## **Usage**

After installation, you can start using LoCoBot by running the main script:

```bash
python3 ./examples/robot_demo.py
```
The `robot_demo.py` script runs a web server on port 5000, allowing you to control the robot and enable object avoidance directly through the web interface.

### Manual Control:
- `W` - Move Forward  
- `A` - Turn Left  
- `S` - Move Backward  
- `D` - Turn Right  

---

## **Documentation**

Comprehensive documentation is available in the [docs/](docs/) directory:

- **System Overview**: Overview of LoCoBot's hardware. [Read More](docs/system_overview.md)
- **PyKobuki**: Library documentation for controlling the Kobuki base. [Read More](docs/PyKobuki.md)
- **WidowX 200 Arm Documentation**: Detailed instructions for using the robot arm library. [Read More](docs/WidowX_200_Arm_Documentation.md)
- **Intel RealSense**: Documentation pending. [Coming Soon](#).

---

## **License**

This project is licensed under the [GPL-3.0 License](LICENSE).

---
