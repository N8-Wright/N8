cmake_minimum_required(VERSION 3.5)
project(N8 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

if(WIN32)
	add_definitions(-D_CRT_SECURE_NO_WARNINGS)
else()
	add_compile_options(-fsanitize=address,undefined)
	add_link_options(-fsanitize=address,undefined)
endif()

add_subdirectory(src)
add_subdirectory(test)
