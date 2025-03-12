# Install script for directory: /home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/locobot/Documents/kobuki/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ecl/converters" TYPE FILE FILES
    "/home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters/char.hpp"
    "/home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters/char_strings.hpp"
    "/home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters/converter.hpp"
    "/home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters/from_byte_array.hpp"
    "/home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters/integers.hpp"
    "/home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters/string.hpp"
    "/home/locobot/Documents/kobuki/src/ecl_core/ecl_converters/include/ecl/converters/to_byte_array.hpp"
    )
endif()

