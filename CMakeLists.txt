cmake_minimum_required(VERSION 2.8.7)

# VelodyneHDL
project(VelodyneHDL)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/modules")

# include cmake scripts
include(cmake/dd-macros.cmake)
include(cmake/dd-testing.cmake)
include(cmake/dd-version.cmake)

find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
option(BUILD_SHARED_LIBS "Build VelodyneHDL with shared libraries." ON)


include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_BINARY_DIR})


find_library(PCAP_LIBRARY pcap DOC "pcap library")
find_path(PCAP_INCLUDE_DIR pcap.h DOC "pcap include directory")
mark_as_advanced(PCAP_LIBRARY PCAP_INCLUDE_DIR)
include_directories(${PCAP_INCLUDE_DIR})



set(Boost_USE_MULTITHREADED ON)
find_package(Boost REQUIRED COMPONENTS system thread regex date_time)
include_directories(${Boost_INCLUDE_DIRS})



set(sources
  vtkVelodyneHDLReader.cxx
  vtkVelodyneHDLSource.cxx
  )

set(VTK_LIBRARIES
  vtkFiltering
  vtkIO
  )

set(deps
  ${PCAP_LIBRARY}
  ${Boost_LIBRARIES}
  ${VTK_LIBRARIES}
  )


set(library_name vtkVelodyneHDL)


add_library(${library_name} ${sources})
target_link_libraries(${library_name} ${deps})

add_executable(PacketFileSender PacketFileSender.cxx)
target_link_libraries(PacketFileSender ${deps})

add_executable(TestReader test/TestReader.cxx)
target_link_libraries(TestReader ${library_name})




#install(TARGETS ${library_name}
#    RUNTIME DESTINATION "${CMAKE_BINARY_DIR}/bin"
#    LIBRARY DESTINATION "${CMAKE_BINARY_DIR}/lib"
#    ARCHIVE DESTINATION "${CMAKE_BINARY_DIR}/lib")

if(VTK_WRAP_PYTHON)
  include_directories(${VTK_PYTHON_INCLUDE_DIR})
  include(${CMAKE_SOURCE_DIR}/cmake/wrap-python.cmake)
  wrap_python(${library_name} "${sources}")
endif()
