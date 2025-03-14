#!/bin/bash
set -e

# Check for required commands and install them if missing
install_dependencies() {
    echo "Checking for required dependencies..."

    # Check if `vcs` is installed
    if ! command -v vcs &>/dev/null; then
        echo "'vcs' is not installed. Installing..."
        sudo apt-get update
        sudo apt-get install -y python3-pip
        pip3 install vcstool
    fi

    # Check if `colcon` is installed
    if ! command -v colcon &>/dev/null; then
        echo "'colcon' is not installed. Installing..."
        pip3 install colcon-common-extensions
    fi

    echo "Installing pybind11..."
    sudo pip3 install pybind11
}

install_dependencies

WORKSPACE_DIR="kobuki"
BASHRC="$HOME/.bashrc"

echo "Creating workspace directory '$WORKSPACE_DIR' (if not exists)..."
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"

echo "Downloading required files..."
wget -O venv.bash "https://raw.githubusercontent.com/kobuki-base/kobuki_documentation/release/1.0.x/resources/venv.bash" || { echo "Failed to download venv.bash"; exit 1; }
wget -O colcon.meta "https://raw.githubusercontent.com/kobuki-base/kobuki_documentation/release/1.0.x/resources/colcon.meta" || { echo "Failed to download colcon.meta"; exit 1; }
wget -O kobuki_standalone.repos "https://raw.githubusercontent.com/kobuki-base/kobuki_documentation/release/1.0.x/resources/kobuki_standalone.repos" || { echo "Failed to download kobuki_standalone.repos"; exit 1; }

echo "Sourcing the virtual environment launcher..."
# This script downloads and installs build tools (colcon, vcstool, etc.) in a virtual environment
source ./venv.bash

echo "Creating 'src' directory and importing repositories..."
mkdir -p src
vcs import ./src < kobuki_standalone.repos || { echo "vcs import failed"; exit 1; }

# Optional: if you prefer to use your system Eigen, uncomment the following line:
# touch src/eigen/AMENT_IGNORE

echo "Deactivating the virtual environment..."
deactivate 2>/dev/null || true

echo "Sourcing the virtual environment again for building..."
source ./venv.bash

echo "Building the Kobuki software (this may take a while)..."
colcon build --merge-install --cmake-args -DBUILD_TESTING=OFF

echo "Build complete. The resulting files are in the './install' directory."

# Optional: Install udev rule for a persistent Kobuki device name.
read -p "Do you want to install the udev rule for Kobuki (requires sudo)? [y/N] " install_udev
if [[ "$install_udev" =~ ^[Yy]$ ]]; then
    echo "Downloading udev rule..."
    wget -O 60-kobuki.rules "https://raw.githubusercontent.com/kobuki-base/kobuki_ftdi/devel/60-kobuki.rules" || { echo "Failed to download 60-kobuki.rules"; exit 1; }
    echo "Copying the udev rule to /etc/udev/rules.d/ (sudo required)..."
    sudo cp 60-kobuki.rules /etc/udev/rules.d/
    echo "Reloading and restarting the udev service..."
    sudo service udev reload
    sudo service udev restart
    echo "udev rule installed. Your Kobuki should now appear as /dev/kobuki when connected."
fi

# This needs improvement but it works so wtv. I know this is never going to be updated
read -p "Do you want to add LD_LIBRARY_PATH exports to your bashrc file? These are needed to work properly. [y/N] " install_exports
if [[ "$install_udev" =~ ^[Yy]$ ]]; then
    # LD_LIBRARY_PATH entries
    LD_PATH_1='export LD_LIBRARY_PATH="$WORKSPACE_DIR/build/kobuki_core/src/driver:$LD_LIBRARY_PATH"'
    LD_PATH_2='export LD_LIBRARY_PATH="$WORKSPACE_DIR/install/lib:$LD_LIBRARY_PATH"'

    # Function to append to .bashrc if not already present
    add_to_bashrc() {
        local line="$1"
        grep -qxF "$line" "$BASHRC" || echo "$line" >> "$BASHRC"
    }

    # Add entries
    add_to_bashrc "$LD_PATH_1"
    add_to_bashrc "$LD_PATH_2"

    # Source .bashrc to apply changes
    source "$BASHRC"
fi

echo "Setup is complete."
echo ""
echo "To check Kobuki version info, run:"
echo "  source ./install/setup.bash && kobuki-version-info"
echo ""
echo "To take Kobuki for a test drive, run:"
echo "  source ./install/setup.bash && kobuki-simple-keyop"

# install pybind, and other shit
# export LD_LIBRARY_PATH=/home/locobot/micro-software/kobuki/build/kobuki_core/src/driver:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/home/locobot/micro-software/kobuki/install/lib:$LD_LIBRARY_PATH