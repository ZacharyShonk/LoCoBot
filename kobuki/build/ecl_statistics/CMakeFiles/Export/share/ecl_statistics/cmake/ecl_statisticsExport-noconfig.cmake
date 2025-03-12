#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ecl_statistics::ecl_statistics" for configuration ""
set_property(TARGET ecl_statistics::ecl_statistics APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(ecl_statistics::ecl_statistics PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libecl_statistics.so.1.2.1"
  IMPORTED_SONAME_NOCONFIG "libecl_statistics.so.1.2.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS ecl_statistics::ecl_statistics )
list(APPEND _IMPORT_CHECK_FILES_FOR_ecl_statistics::ecl_statistics "${_IMPORT_PREFIX}/lib/libecl_statistics.so.1.2.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
