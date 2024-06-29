include(FetchContent)
FetchContent_Declare(
	googletest
	GIT_REPOSITORY https://github.com/google/googletest.git
	GIT_TAG        v1.14.0
)

if (WIN32)
   set(gtest_force_shared_crt ON CACHE BOOL "Always use the shared crt runtime library" FORCE)
endif()

FetchContent_MakeAvailable(googletest)

enable_testing()
include(GoogleTest)

add_executable(KVStoreTests $<TARGET_OBJECTS:N8Objects> KVStoreTests.cpp)
target_link_libraries(KVStoreTests GTest::gtest_main)
target_include_directories(KVStoreTests PRIVATE "../src")
gtest_discover_tests(KVStoreTests)

target_compile_options(KVStoreTests PRIVATE
	"$<$<CONFIG:Debug>:${N8_COMPILE_OPTIONS_DEBUG}>"
	"$<$<CONFIG:RelWithDebInfo>:${N8_COMPILE_OPTIONS_DEBUG}>"
	"$<$<CONFIG:Release>:${N8_COMPILE_OPTIONS_RELEASE}>"
	"$<$<CONFIG:MinSizeRel>:${N8_COMPILE_OPTIONS_RELEASE}>"
)
target_link_options(KVStoreTests PRIVATE
	"$<$<CONFIG:Debug>:${N8_LINK_OPTIONS_DEBUG}>"
	"$<$<CONFIG:RelWithDebInfo>:${N8_LINK_OPTIONS_DEBUG}>"
	"$<$<CONFIG:Release>:${N8_LINK_OPTIONS}>"
	"$<$<CONFIG:MinSizeRel>:${N8_LINK_OPTIONS}>"
)
