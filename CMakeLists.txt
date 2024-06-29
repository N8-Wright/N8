cmake_minimum_required(VERSION 3.5)
project(N8 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)


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
		-fno-strict-aliasing -ftrivial-auto-var-init=zero
	)
endif()

add_subdirectory(src)
add_subdirectory(test)
