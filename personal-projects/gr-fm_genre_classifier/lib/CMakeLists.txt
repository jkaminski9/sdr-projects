# Copyright 2011,2012,2016,2018,2019 Free Software Foundation, Inc.
#
# This file was generated by gr_modtool, a tool from the GNU Radio framework
# This file is a part of gr-fm_genre_classifier
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

list(APPEND fm_genre_classifier_sources
)

set(fm_genre_classifier_sources "${fm_genre_classifier_sources}" PARENT_SCOPE)
if(NOT fm_genre_classifier_sources)
    MESSAGE(STATUS "No C++ sources... skipping lib/")
    return()
endif(NOT fm_genre_classifier_sources)

add_library(gnuradio-fm_genre_classifier SHARED ${fm_genre_classifier_sources})
target_link_libraries(gnuradio-fm_genre_classifier gnuradio::gnuradio-runtime)
target_include_directories(gnuradio-fm_genre_classifier
    PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include>
    PUBLIC $<INSTALL_INTERFACE:include>
  )
set_target_properties(gnuradio-fm_genre_classifier PROPERTIES DEFINE_SYMBOL "gnuradio_fm_genre_classifier_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-fm_genre_classifier PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-fm_genre_classifier)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

# If your unit tests require special include paths, add them here
#include_directories()
# List all files that contain Boost.UTF unit tests here
list(APPEND test_fm_genre_classifier_sources
)
# Anything we need to link to for the unit tests go here
list(APPEND GR_TEST_TARGET_DEPS gnuradio-fm_genre_classifier)

if(NOT test_fm_genre_classifier_sources)
    MESSAGE(STATUS "No C++ unit tests... skipping")
    return()
endif(NOT test_fm_genre_classifier_sources)

foreach(qa_file ${test_fm_genre_classifier_sources})
    GR_ADD_CPP_TEST("fm_genre_classifier_${qa_file}"
        ${CMAKE_CURRENT_SOURCE_DIR}/${qa_file}
    )
endforeach(qa_file)
