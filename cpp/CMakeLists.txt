cmake_minimum_required(VERSION 2.8.12)
project(Mic)

add_definitions("-std=c++11")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(Mic mic.cpp)
target_include_directories(Mic PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_link_libraries(Mic 
${CMAKE_SOURCE_DIR}/libportaudio.a
pthread
rt
m
asound
jack
)
target_link_libraries(Mic ${CONAN_LIBS})