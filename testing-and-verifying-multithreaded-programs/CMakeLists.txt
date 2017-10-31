cmake_minimum_required(VERSION 3.5.1)

#if(DEFINED ${BUILD_DEMOS})
   add_subdirectory(demos/state-space-explorer)
#endif(DEFINED ${BUILD_DEMOS})

set(RR_TEST_PROGRAMS    demos/state-space-explorer/libs/record-replay/tests/test_programs)
set(SSE_TEST_PROGRAMS   demos/state-space-explorer/tests/test_programs)

configure_file(${RR_TEST_PROGRAMS}/real_world/background_thread.cpp 
               demos/programs/background_thread.cpp COPYONLY)
configure_file(${RR_TEST_PROGRAMS}/real_world/bank_account.cpp
               demos/programs/bank_account.cpp COPYONLY)
