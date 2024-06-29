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


		    
