
//--------------------------------------------------------------------------------------------------
/// @file dining-philosophers.cpp
/// @detail Classic scenario where a number of philosophers are at a dining table. After thinking
/// for a while each philosopher tries to eat their spaghetti. For that they need two forks: the
/// one to their left, and the one to their right. Each of the forks can be held by one philosopher
/// at a time.
/// @note This program has a potential deadlock.
/// @author Susanne van den Elsen
/// @date 2017
//--------------------------------------------------------------------------------------------------

#include <thread>

//--------------------------------------------------------------------------------------------------

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
