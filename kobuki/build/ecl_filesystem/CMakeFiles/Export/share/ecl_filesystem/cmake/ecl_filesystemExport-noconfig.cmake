#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ecl_filesystem::ecl_filesystem" for configuration ""
set_property(TARGET ecl_filesystem::ecl_filesystem APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(ecl_filesystem::ecl_filesystem PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libecl_filesystem.so.1.2.1"
  IMPORTED_SONAME_NOCONFIG "libecl_filesystem.so.1.2.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS ecl_filesystem::ecl_filesystem )
list(APPEND _IMPORT_CHECK_FILES_FOR_ecl_filesystem::ecl_filesystem "${_IMPORT_PREFIX}/lib/libecl_filesystem.so.1.2.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
