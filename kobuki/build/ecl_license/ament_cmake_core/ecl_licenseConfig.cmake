# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_ecl_license_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED ecl_license_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(ecl_license_FOUND FALSE)
  elseif(NOT ecl_license_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(ecl_license_FOUND FALSE)
  endif()
  return()
endif()
set(_ecl_license_CONFIG_INCLUDED TRUE)

# output package information
if(NOT ecl_license_FIND_QUIETLY)
  message(STATUS "Found ecl_license: 1.0.3 (${ecl_license_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'ecl_license' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${ecl_license_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(ecl_license_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_libraries-extras.cmake")
foreach(_extra ${_extras})
  include("${ecl_license_DIR}/${_extra}")
endforeach()
