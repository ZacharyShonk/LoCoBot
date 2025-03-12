# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_ecl_converters_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED ecl_converters_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(ecl_converters_FOUND FALSE)
  elseif(NOT ecl_converters_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(ecl_converters_FOUND FALSE)
  endif()
  return()
endif()
set(_ecl_converters_CONFIG_INCLUDED TRUE)

# output package information
if(NOT ecl_converters_FIND_QUIETLY)
  message(STATUS "Found ecl_converters: 1.2.1 (${ecl_converters_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'ecl_converters' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${ecl_converters_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(ecl_converters_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_targets-extras.cmake;ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_dependencies-extras.cmake")
foreach(_extra ${_extras})
  include("${ecl_converters_DIR}/${_extra}")
endforeach()
