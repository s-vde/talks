
//--------------------------------------------------------------------------------------------------
/// @file simple_deadlock.cpp
//--------------------------------------------------------------------------------------------------

#include <mutex>
#include <thread>

int main()
{
   std::mutex m1, m2;
   
   std::thread thr1([&m1, &m2]{
      std::lock_guard<std::mutex> lock1(m1);
      std::lock_guard<std::mutex> lock2(m2);
   });
   
   std::thread thr2([&m1, &m2]{
      std::lock_guard<std::mutex> lock2(m2);
      std::lock_guard<std::mutex> lock1(m1);
   });
   
   thr1.join();
   thr2.join();

   return 0;
}

//--------------------------------------------------------------------------------------------------
