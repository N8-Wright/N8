add_library(N8Objects OBJECT
		      KVStore.hpp
		      KVStore.cpp
)


add_executable(test test.cpp $<TARGET_OBJECTS:N8Objects>)
		    
