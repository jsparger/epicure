#FindPVAccessCPP.cmake
#
# Finds the EPICS pvaccesscpp library
#
# This will define the following variables
#
#    PVAccessCPP_FOUND
#    PVAccessCPP_INCLUDE_DIRS
#
# and the following imported targets
#
#     PVAccessCPP::PVAccessCPP
#

# find dependencies
# find_package(PVDataCPP)
# if(NOT PVDataCPP_FOUND)
#   message(FATAL_ERROR "PVDataCPP not found")
# endif()
#
# find_package(EPICSBase)
# if(NOT EPICSBase_FOUND)
#   message(FATAL_ERROR "EPICS Base not found")
# endif()

# figure out the module directory. It could include version numbers
file(GLOB_RECURSE PVAccess_H $ENV{EPICS_MODULES_PATH}/pvAccessCPP/*pvAccess.h)
if(NOT PVAccess_H)
  message(FATAL_ERROR "pvAccess.h not found under $EPICS_MODULES_PATH")
endif()
message(${PVAccess_H})
get_filename_component(PVAccess_H_Dir ${PVAccess_H} DIRECTORY)
set(PVAccessCPP_Module_Dir "${PVAccess_H_Dir}/../..")

# set the include directory
set(PVAccessCPP_INCLUDE_DIRS "${PVAccessCPP_Module_Dir}/include")

# find the pvaccess cpp shared library
set(PVAccessCPP_LIB_DIR "${PVAccessCPP_Module_Dir}/lib/$ENV{EPICS_HOST_ARCH}")
find_library(PVAccessCPP_LIB pvAccessCPP PATHS ${PVAccessCPP_LIB_DIR})
if(NOT PVAccessCPP_LIB)
  message(FATAL_ERROR "pvAccessCPP shared library not found at ${PVAccessCPP_LIB_DIR}")
endif()

add_library(PVAccessCPP::PVAccessCPP INTERFACE IMPORTED)
set_target_properties(PVAccessCPP::PVAccessCPP PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "${PVAccessCPP_INCLUDE_DIRS}"
  INTERFACE_LINK_LIBRARIES "${PVAccessCPP_LIB}"
)
# target_link_libraries(PVAccessCPP::PVAccessCPP
#   PUBLIC PVDataCPP::PVDataCPP
#   PUBLIC EPICSBase::EPICSBase
# )

# if we made it this far, then we found the module
set(PVAccessCPP_FOUND TRUE)
message(${PVAccessCPP_Module_Dir})
