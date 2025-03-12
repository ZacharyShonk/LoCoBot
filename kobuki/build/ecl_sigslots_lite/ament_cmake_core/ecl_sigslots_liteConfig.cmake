# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_ecl_sigslots_lite_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED ecl_sigslots_lite_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(ecl_sigslots_lite_FOUND FALSE)
  elseif(NOT ecl_sigslots_lite_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(ecl_sigslots_lite_FOUND FALSE)
  endif()
  return()
endif()
set(_ecl_sigslots_lite_CONFIG_INCLUDED TRUE)

# output package information
if(NOT ecl_sigslots_lite_FIND_QUIETLY)
  message(STATUS "Found ecl_sigslots_lite: 1.1.0 (${ecl_sigslots_lite_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'ecl_sigslots_lite' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${ecl_sigslots_lite_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(ecl_sigslots_lite_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_targets-extras.cmake;ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_dependencies-extras.cmake")
foreach(_extra ${_extras})
  include("${ecl_sigslots_lite_DIR}/${_extra}")
endforeach()
