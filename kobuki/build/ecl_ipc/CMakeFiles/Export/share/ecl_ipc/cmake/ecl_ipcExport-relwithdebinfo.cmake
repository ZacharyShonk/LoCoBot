#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ecl_ipc::ecl_ipc" for configuration "RelWithDebInfo"
set_property(TARGET ecl_ipc::ecl_ipc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ecl_ipc::ecl_ipc PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libecl_ipc.so.1.2.1"
  IMPORTED_SONAME_RELWITHDEBINFO "libecl_ipc.so.1.2.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS ecl_ipc::ecl_ipc )
list(APPEND _IMPORT_CHECK_FILES_FOR_ecl_ipc::ecl_ipc "${_IMPORT_PREFIX}/lib/libecl_ipc.so.1.2.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
