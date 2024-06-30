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


add_executable(Website $<TARGET_OBJECTS:N8Objects> Website.cpp)
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

target_link_libraries(Website PRIVATE Crow::Crow)
