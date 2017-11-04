
//--------------------------------------------------------------------------------------------------
/// @file simple_deadlock.cpp
//--------------------------------------------------------------------------------------------------

#include <atomic>
#include <mutex>
#include <thread>

int main()
{
   std::atomic<bool> b{false};
   std::mutex m1, m2;
   
   std::thread thr1([&b, &m1, &m2]{
      std::lock_guard<std::mutex> lock1(m1);
      while (!b) {}
      std::lock_guard<std::mutex> lock2(m2);
   });
   
   std::thread thr2([&b, &m1, &m2]{
      std::lock_guard<std::mutex> lock2(m2);
      b = true;
      std::lock_guard<std::mutex> lock1(m1);
   });
   
   thr1.join();
   thr2.join();

   return 0;
}

//--------------------------------------------------------------------------------------------------
