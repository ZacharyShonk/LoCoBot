#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ecl_formatters::ecl_formatters" for configuration ""
set_property(TARGET ecl_formatters::ecl_formatters APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(ecl_formatters::ecl_formatters PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libecl_formatters.so.1.2.1"
  IMPORTED_SONAME_NOCONFIG "libecl_formatters.so.1.2.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS ecl_formatters::ecl_formatters )
list(APPEND _IMPORT_CHECK_FILES_FOR_ecl_formatters::ecl_formatters "${_IMPORT_PREFIX}/lib/libecl_formatters.so.1.2.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
