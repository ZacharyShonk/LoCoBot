##############################################################################
# Enable
##############################################################################

# Enable CXX17 and abort if not available
macro(ecl_enable_cxx17_compiler)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)  # aborts with an error if the requested standard is not available
  set(CMAKE_CXX_EXTENSIONS OFF)  # if ON, it will use gnu++17 instead of std++17
  set(CMAKE_CXX_STANDARD 17)
endmacro()

# Enable CXX14 and abort if not available
macro(ecl_enable_cxx14_compiler)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)  # aborts with an error if the requested standard is not available
  set(CMAKE_CXX_EXTENSIONS OFF)  # if ON, it will use gnu++14 instead of std++14
  set(CMAKE_CXX_STANDARD 14)
endmacro()

# Enable CXX11 and abort if not available
macro(ecl_enable_cxx11_compiler)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)  # aborts with an error if the requested standard is not available
  set(CMAKE_CXX_EXTENSIONS OFF)  # if ON, it will use gnu++11 instead of std++11
  set(CMAKE_CXX_STANDARD 11)
endmacro()

# Enable the kitchen sink, i.e. as much as possible.
macro(ecl_enable_cxx_warnings)
  if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Werror -Wpedantic)
  endif()
endmacro()

