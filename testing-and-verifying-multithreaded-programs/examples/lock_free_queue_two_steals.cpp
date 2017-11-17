
//-----------------------------------------------------------------------------------------------100
/// @file lock_free_queue_two_steals.cpp
/// @author Susanne van den Elsen
/// @date 2017
//--------------------------------------------------------------------------------------------------

#define SIZE 2

#include "lock_free_queue.cpp"

#include <cassert>


int main()
{
   lock_free_queue queue;
   
   int job1, job2 = -2;

   std::thread worker1([&queue, &job1]{
      job1 = queue.steal();
   });
   
   std::thread worker2([&queue, &job2]{
      job2 = queue.steal();
   });
   
   queue.push(0);
   queue.push(1);
   
   worker1.join();
   worker2.join();
   
   assert(job1 == -1 || job1 != job2);

   return 0;
}
