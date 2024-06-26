cmake_minimum_required(VERSION 3.5)
project(N8 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

file(
  DOWNLOAD
  https://github.com/cpm-cmake/CPM.cmake/releases/download/v0.40.0/CPM.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/cmake/CPM.cmake
  EXPECTED_HASH SHA256=7b354f3a5976c4626c876850c93944e52c83ec59a159ae5de5be7983f0e17a2a
)
include(${CMAKE_CURRENT_BINARY_DIR}/cmake/CPM.cmake)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(WIN32)
	add_definitions(-D_CRT_SECURE_NO_WARNINGS)
else()

	set(N8_COMPILE_OPTIONS
	
		-Wall -Wextra -Wformat -Wformat=2 -Wconversion -Wsign-conversion
		-Wimplicit-fallthrough -Werror=format-security -Werror=implicit
		-Werror=incompatible-pointer-types -Werror=int-conversion
		-U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=3
		-D_GLIBCXX_ASSERTIONS
		-fstack-protector-strong 
		-Wno-unqualified-std-cast-call
	)

	if (CMAKE_SYSTEM_PROCESSOR MATCHES "(x86)|(X86)|(amd64)|(AMD64)")
	   set (N8_COMPILE_OPTIONS ${N8_COMPILE_OPTIONS}
	       -fcf-protection=full
	   )
	else ()
	   set (N8_COMPILE_OPTIONS ${N8_COMPILE_OPTIONS}
	       -mbranch-protection=standard	   
	   )	   
	endif ()

	# Options that are only useful when compiling the full executable
	set(N8_LINK_OPTIONS "")

	set(N8_COMPILE_OPTIONS_DEBUG ${N8_COMPILE_OPTIONS} "-fsanitize=address,undefined")
	set(N8_LINK_OPTIONS_DEBUG ${N8_LINK_OPTIONS} -fsanitize=address,undefined)
	set(N8_COMPILE_OPTIONS_RELEASE ${N8_COMPILE_OPTIONS}
		-O3 -fno-delete-null-pointer-checks -fno-strict-overflow
		-fno-strict-aliasing
	)
endif()

add_subdirectory(src)
add_subdirectory(test)
