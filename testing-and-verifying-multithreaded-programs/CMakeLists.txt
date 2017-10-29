cmake_minimum_required(VERSION 3.5.2)

add_subdirectory(demos/state-space-explorer)

set(TEST_PROGRAMS    demos/state-space-explorer/libs/record-replay/tests/test_programs)

configure_file(${TEST_PROGRAMS}/real_world/background_thread.cpp 
               demos/programs/background_thread.cpp COPYONLY)
               
configure_file(${TEST_PROGRAMS}/real_world/dining_philosophers.cpp 
               demos/programs/dining_philosophers.cpp COPYONLY)

configure_file(examples/simple_data_race.cpp 
               demos/programs/simple_data_race.cpp COPYONLY)
                              
configure_file(examples/trivial_deadlock.cpp 
               demos/programs/trivial_deadlock.cpp COPYONLY)