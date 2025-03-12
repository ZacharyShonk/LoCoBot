#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ecl_geometry::ecl_geometry" for configuration ""
set_property(TARGET ecl_geometry::ecl_geometry APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(ecl_geometry::ecl_geometry PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libecl_geometry.so.1.2.1"
  IMPORTED_SONAME_NOCONFIG "libecl_geometry.so.1.2.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS ecl_geometry::ecl_geometry )
list(APPEND _IMPORT_CHECK_FILES_FOR_ecl_geometry::ecl_geometry "${_IMPORT_PREFIX}/lib/libecl_geometry.so.1.2.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
