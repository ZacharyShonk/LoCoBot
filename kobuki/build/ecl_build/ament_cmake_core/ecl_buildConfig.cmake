# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_ecl_build_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED ecl_build_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(ecl_build_FOUND FALSE)
  elseif(NOT ecl_build_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(ecl_build_FOUND FALSE)
  endif()
  return()
endif()
set(_ecl_build_CONFIG_INCLUDED TRUE)

# output package information
if(NOT ecl_build_FIND_QUIETLY)
  message(STATUS "Found ecl_build: 1.0.3 (${ecl_build_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'ecl_build' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${ecl_build_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(ecl_build_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ecl_platform_detection.cmake;ecl_package.cmake;ecl_find_sse.cmake;ecl_build_utilities.cmake;ecl_cxx.cmake;cotire.cmake")
foreach(_extra ${_extras})
  include("${ecl_build_DIR}/${_extra}")
endforeach()
