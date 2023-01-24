INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_FM_GENRE_CLASSIFIER fm_genre_classifier)

FIND_PATH(
    FM_GENRE_CLASSIFIER_INCLUDE_DIRS
    NAMES fm_genre_classifier/api.h
    HINTS $ENV{FM_GENRE_CLASSIFIER_DIR}/include
        ${PC_FM_GENRE_CLASSIFIER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FM_GENRE_CLASSIFIER_LIBRARIES
    NAMES gnuradio-fm_genre_classifier
    HINTS $ENV{FM_GENRE_CLASSIFIER_DIR}/lib
        ${PC_FM_GENRE_CLASSIFIER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/fm_genre_classifierTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FM_GENRE_CLASSIFIER DEFAULT_MSG FM_GENRE_CLASSIFIER_LIBRARIES FM_GENRE_CLASSIFIER_INCLUDE_DIRS)
MARK_AS_ADVANCED(FM_GENRE_CLASSIFIER_LIBRARIES FM_GENRE_CLASSIFIER_INCLUDE_DIRS)
