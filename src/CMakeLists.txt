find_package(Threads REQUIRED)
CPMAddPackage("gh:chriskohlhoff/asio#asio-1-30-2")
if(asio_ADDED)
	add_library(asio INTERFACE)
	target_include_directories(asio SYSTEM INTERFACE ${asio_SOURCE_DIR}/asio/include)
	target_compile_definitions(asio INTERFACE ASIO_STANDALONE)
	target_link_libraries(asio INTERFACE Threads::Threads)

	add_library(asio::asio ALIAS asio)
endif()

CPMAddPackage(
	NAME Crow
	GITHUB_REPOSITORY CrowCpp/Crow
	GIT_TAG v1.2.0
	VERSION 1.2.0
	OPTIONS "CROW_BUILD_EXAMPLES OFF" "CROW_BUILD_TESTS OFF" "CROW_INSTALL OFF"
)

CPMAddPackage(
	NAME md4c
	GITHUB_REPOSITORY mity/md4c
	GIT_TAG release-0.5.2
	VERSION 0.5.2
	OPTIONS "BUILD_MD2HTML_EXECUTABLE OFF"
)
if (md4c_ADDED)
	# Make sure we can include md4c.h and md4c-html.h when linking against cmake targets.
	target_include_directories(md4c SYSTEM INTERFACE $<BUILD_INTERFACE:${md4c_SOURCE_DIR}/src>)
endif()

add_library(N8Objects STATIC
		      KVStore.hpp
		      KVStore.cpp
)

target_compile_options(N8Objects PRIVATE
	"$<$<CONFIG:Debug>:${N8_COMPILE_OPTIONS_DEBUG}>"
	"$<$<CONFIG:RelWithDebInfo>:${N8_COMPILE_OPTIONS_DEBUG}>"
	"$<$<CONFIG:Release>:${N8_COMPILE_OPTIONS_RELEASE}>"
	"$<$<CONFIG:MinSizeRel>:${N8_COMPILE_OPTIONS_RELEASE}>"
)
target_link_options(N8Objects PRIVATE
	"$<$<CONFIG:Debug>:${N8_LINK_OPTIONS_DEBUG}>"
	"$<$<CONFIG:RelWithDebInfo>:${N8_LINK_OPTIONS_DEBUG}>"
	"$<$<CONFIG:Release>:${N8_LINK_OPTIONS}>"
	"$<$<CONFIG:MinSizeRel>:${N8_LINK_OPTIONS}>"
)


add_executable(Website $<TARGET_OBJECTS:N8Objects>
		       Website.cpp
		       BlogController.cpp
		       BlogController.hpp
)
target_compile_options(Website PRIVATE
	"$<$<CONFIG:Debug>:${N8_COMPILE_OPTIONS_DEBUG}>"
	"$<$<CONFIG:RelWithDebInfo>:${N8_COMPILE_OPTIONS_DEBUG}>"
	"$<$<CONFIG:Release>:${N8_COMPILE_OPTIONS_RELEASE}>"
	"$<$<CONFIG:MinSizeRel>:${N8_COMPILE_OPTIONS_RELEASE}>"
)
target_link_options(Website PRIVATE
	"$<$<CONFIG:Debug>:${N8_LINK_OPTIONS_DEBUG}>"
	"$<$<CONFIG:RelWithDebInfo>:${N8_LINK_OPTIONS_DEBUG}>"
	"$<$<CONFIG:Release>:${N8_LINK_OPTIONS}>"
	"$<$<CONFIG:MinSizeRel>:${N8_LINK_OPTIONS}>"
)

target_link_libraries(Website PRIVATE Crow::Crow md4c-html)
