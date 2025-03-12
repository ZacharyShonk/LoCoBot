#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "kobuki_core::kobuki_core" for configuration ""
set_property(TARGET kobuki_core::kobuki_core APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(kobuki_core::kobuki_core PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libkobuki_core.so.1.3.1"
  IMPORTED_SONAME_NOCONFIG "libkobuki_core.so.1.3.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS kobuki_core::kobuki_core )
list(APPEND _IMPORT_CHECK_FILES_FOR_kobuki_core::kobuki_core "${_IMPORT_PREFIX}/lib/libkobuki_core.so.1.3.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
