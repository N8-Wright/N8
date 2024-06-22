include(FetchContent)
FetchContent_Declare(
	googletest
	GIT_REPOSITORY https://github.com/google/googletest.git
	GIT_TAG        v1.14.0
)

FetchContent_MakeAvailable(googletest)

enable_testing()
include(GoogleTest)

add_executable(KVStoreTests $<TARGET_OBJECTS:N8Objects> KVStoreTests.cpp)
target_link_libraries(KVStoreTests GTest::gtest_main)
target_include_directories(KVStoreTests PRIVATE "../src")
gtest_discover_tests(KVStoreTests)

