# Install script for directory: /home/locobot/Documents/kobuki/src/eigen/Eigen

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

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/Eigen" TYPE FILE FILES
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Cholesky"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/CholmodSupport"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Core"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Dense"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Eigen"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Eigenvalues"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Geometry"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Householder"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/IterativeLinearSolvers"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Jacobi"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/LU"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/MetisSupport"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/OrderingMethods"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/PaStiXSupport"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/PardisoSupport"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/QR"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/QtAlignedMalloc"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/SPQRSupport"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/SVD"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/Sparse"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/SparseCholesky"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/SparseCore"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/SparseLU"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/SparseQR"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/StdDeque"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/StdList"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/StdVector"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/SuperLUSupport"
    "/home/locobot/Documents/kobuki/src/eigen/Eigen/UmfPackSupport"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/Eigen" TYPE DIRECTORY FILES "/home/locobot/Documents/kobuki/src/eigen/Eigen/src" FILES_MATCHING REGEX "/[^/]*\\.h$")
endif()

