#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ecl_io::ecl_io" for configuration ""
set_property(TARGET ecl_io::ecl_io APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(ecl_io::ecl_io PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libecl_io.so.1.1.0"
  IMPORTED_SONAME_NOCONFIG "libecl_io.so.1.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS ecl_io::ecl_io )
list(APPEND _IMPORT_CHECK_FILES_FOR_ecl_io::ecl_io "${_IMPORT_PREFIX}/lib/libecl_io.so.1.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
