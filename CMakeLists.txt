cmake_minimum_required(VERSION 3.5)
project(N8 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

add_compile_options(-fsanitize=address,undefined)
add_link_options(-fsanitize=address,undefined)

add_subdirectory(src)
