#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // for automatic STL conversions
#include <string>
#include <stdexcept>
#include <thread>
#include <chrono>
#include <cmath>    // For M_PI
#include <memory>
#include <iomanip>  // For std::fixed and std::setprecision
#include <sstream>  // For std::ostringstream

// Include the Kobuki headers and ECL exceptions.
#include <kobuki_core/kobuki.hpp>
#include <ecl/exceptions/standard_exception.hpp>

namespace py = pybind11;

class PyKobuki {
public:
    // Constructor: initializes the Kobuki robot.
    PyKobuki(const std::string &device = "/dev/kobuki") {
        // Create the robot object with the default constructor.
        kobuki_ = std::make_unique<kobuki::Kobuki>();

        // Set up parameters.
        kobuki::Parameters parameters;
        parameters.device_port = device;
        // Additional parameters can be set here if needed.

        // Attempt to initialize the robot with parameters.
        try {
            kobuki_->init(parameters);
        } catch (const ecl::StandardException &e) {
            throw std::runtime_error(e.what());
        }
    }
    
    // Command the robot to move with specified linear and angular velocities.
    void move(double linear, double angular) {
        kobuki_->setBaseControl(linear, angular);
    }
    
    // Sleep function using std::this_thread::sleep_for.
    void sleep(double seconds) {
        std::this_thread::sleep_for(std::chrono::duration<double>(seconds));
    }
    
    // Helper function to format floating-point numbers to two decimal places.
    std::string format_float(double value) const {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << value;
        return oss.str();
    }

    // Read sensor data from the robot.
    // Returns a Python dictionary containing formatted sensor readings.
    py::dict read_sensor_data() const {
        // Get the core sensor data.
        kobuki::CoreSensors::Data data = kobuki_->getCoreSensorData();
        py::dict result;
        result["time_stamp"]    = data.time_stamp;
        result["bumper"]        = data.bumper;
        result["wheel_drop"]    = data.wheel_drop;
        result["cliff"]         = data.cliff;
        result["left_encoder"]  = data.left_encoder;
        result["right_encoder"] = data.right_encoder;
        result["left_pwm"]      = data.left_pwm;
        result["right_pwm"]     = data.right_pwm;
        result["buttons"]       = data.buttons;
        result["charger"]       = data.charger;
        result["battery"]       = format_float(data.battery); // Format battery voltage
        result["over_current"]  = data.over_current;
        return result;
    }
    
    // Shutdown the robot.
    void shutdown() {
        kobuki_->setBaseControl(0, 0);
        kobuki_->disable();
    }
    
private:
    std::unique_ptr<kobuki::Kobuki> kobuki_;
};

PYBIND11_MODULE(pykobuki, m) {
    m.doc() = "Python wrapper for the Kobuki robot using libkobuki";
    
    // Bind the PyKobuki class.
    py::class_<PyKobuki>(m, "Kobuki")
        .def(py::init<const std::string &>(), py::arg("device")="/dev/kobuki",
             "Create a Kobuki object and establish a connection to the robot.")
        .def("move", &PyKobuki::move,
             "Command the robot to move with specified linear and angular velocities.")
        .def("sleep", &PyKobuki::sleep,
             "Sleep for a given number of seconds.")
        .def("read_sensor_data", &PyKobuki::read_sensor_data,
             "Read sensor data (e.g., bumpers, wheel drop, cliff sensors, etc.) from the robot.")
        .def("shutdown", &PyKobuki::shutdown,
             "Shutdown the robot.");
}