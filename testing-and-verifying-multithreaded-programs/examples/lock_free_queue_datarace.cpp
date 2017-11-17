
//-----------------------------------------------------------------------------------------------100
/// @file lock_free_queue_datarace.cpp
/// @author Susanne van den Elsen
/// @date 2017
//--------------------------------------------------------------------------------------------------

#define SIZE 2

#include "lock_free_queue.cpp"


int main()
{
   lock_free_queue queue;

   std::thread worker([&queue]{
      const auto job = queue.steal();
   });
   
   queue.push(0);
   queue.push(1);
   queue.push(2);
   
   worker.join();

   return 0;
}
