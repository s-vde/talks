
//--------------------------------------------------------------------------------------------------
/// @file simple_deadlock.cpp
//--------------------------------------------------------------------------------------------------

#include <thread>

int main()
{
   std::atomic<bool> b{false};
   pthread_mutex_t m1;
   pthread_mutex_t m2;
   
   pthread_mutex_init(&m1, nullptr);
   pthread_mutex_init(&m2, nullptr);
   
   std::thread thr1([&b, &m1, &m2]{
      pthread_mutex_lock(&m1);
      while (!b) {}
      pthread_mutex_lock(&m2);
      pthread_mutex_unlock(&m2);
      pthread_mutex_unlock(&m1);
   });
   
   std::thread thr2([&b, &m1, &m2]{
      pthread_mutex_lock(&m2);
      b = true;
      pthread_mutex_lock(&m1);
      pthread_mutex_unlock(&m1);
      pthread_mutex_unlock(&m2);
   });
   
   thr1.join();
   thr2.join();

   return 0;
}

//--------------------------------------------------------------------------------------------------
