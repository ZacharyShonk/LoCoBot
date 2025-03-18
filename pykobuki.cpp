#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // for automatic STL conversions
#include <string>
#include <stdexcept>
#include <thread>
#include <chrono>
#include <cmath> // For M_PI
#include <memory>
#include <iomanip> // For std::fixed and std::setprecision
#include <sstream> // For std::ostringstream
#include <unordered_map>

// Include the Kobuki headers and ECL exceptions.
#include <kobuki_core/kobuki.hpp>
#include <ecl/exceptions/standard_exception.hpp>

namespace py = pybind11;

class PyKobuki
{
public:
    // Constructor: initializes the Kobuki robot.
    PyKobuki(const std::string &device = "/dev/kobuki")
    {
        kobuki_ = std::make_unique<kobuki::Kobuki>();

        // Set up parameters.
        kobuki::Parameters parameters;
        parameters.device_port = device;

        // Attempt to initialize the robot.
        try
        {
            kobuki_->init(parameters);
        }
        catch (const ecl::StandardException &e)
        {
            throw std::runtime_error(e.what());
        }
    }

    // Command the robot to move with specified linear and angular velocities.
    void move(double linear, double angular)
    {
        kobuki_->setBaseControl(linear, angular);
    }

    // Helper function to format floating-point numbers to two decimal places.
    std::string format_float(double value) const
    {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << value;
        return oss.str();
    }

    // Read sensor data from the robot.
    // Returns a Python dictionary containing formatted sensor readings.
    py::dict read_sensor_data() const
    {
        kobuki::CoreSensors::Data data = kobuki_->getCoreSensorData();
        py::dict result;

        result["time_stamp"] = data.time_stamp;

        // Bumper flags
        result["bumper_left"] = static_cast<bool>(data.bumper & 0x04);
        result["bumper_center"] = static_cast<bool>(data.bumper & 0x02);
        result["bumper_right"] = static_cast<bool>(data.bumper & 0x01);

        // Wheel drop flags
        result["wheel_drop_left"] = static_cast<bool>(data.wheel_drop & 0x02);
        result["wheel_drop_right"] = static_cast<bool>(data.wheel_drop & 0x01);

        // Cliff sensors
        result["cliff_left"] = static_cast<bool>(data.cliff & 0x04);
        result["cliff_center"] = static_cast<bool>(data.cliff & 0x02);
        result["cliff_right"] = static_cast<bool>(data.cliff & 0x01);

        // Encoders
        result["left_encoder"] = data.left_encoder;
        result["right_encoder"] = data.right_encoder;

        // Motor PWM values
        result["left_pwm"] = static_cast<int>(data.left_pwm);
        result["right_pwm"] = static_cast<int>(data.right_pwm);

        // Button flags
        result["button0"] = static_cast<bool>(data.buttons & 0x01);
        result["button1"] = static_cast<bool>(data.buttons & 0x02);
        result["button2"] = static_cast<bool>(data.buttons & 0x04);

        // Charger state
        result["charger_state"] = data.charger;

        // Battery voltage (formatted)
        result["battery_voltage"] = format_float(data.battery * 0.1);

        // Overcurrent flags
        result["overcurrent_left"] = static_cast<bool>(data.over_current & 0x01);
        result["overcurrent_right"] = static_cast<bool>(data.over_current & 0x02);

        return result;
    }

    // Shutdown the robot.
    void shutdown()
    {
        kobuki_->setBaseControl(0, 0);
        kobuki_->disable();
    }

private:
    std::unique_ptr<kobuki::Kobuki> kobuki_;
};

PYBIND11_MODULE(pykobuki, m)
{
    m.doc() = "Python wrapper for the Kobuki robot using libkobuki";

    // Bind the PyKobuki class.
    py::class_<PyKobuki>(m, "Kobuki")
        .def(py::init<const std::string &>(), py::arg("device") = "/dev/kobuki",
             "Create a Kobuki object and establish a connection to the robot.")
        .def("move", &PyKobuki::move,
             "Command the robot to move with specified linear and angular velocities.")
        .def("read_sensor_data", &PyKobuki::read_sensor_data,
             "Read sensor data (e.g., bumpers, wheel drop, cliff sensors, etc.) from the robot.")
        .def("shutdown", &PyKobuki::shutdown,
             "Shutdown the robot.");
}