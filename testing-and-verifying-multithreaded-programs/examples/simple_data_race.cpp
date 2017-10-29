
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
   int x = 0;
   
   std::thread thr1([&x]{
      x = 1;
   });
   
   std::thread thr2([&x]{
      x = 2;
   });
   
   thr1.join();
   thr2.join();

   return 0;
}

//--------------------------------------------------------------------------------------------------
