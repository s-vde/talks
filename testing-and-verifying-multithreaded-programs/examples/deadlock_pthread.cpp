
//--------------------------------------------------------------------------------------------------
/// @file simple_deadlock_pthread.cpp
//--------------------------------------------------------------------------------------------------

#include <pthread.h>
#include <thread>

pthread_t thr1, thr2;
pthread_mutex_t m1, m2;

void* thread1(void* arg)
{
   pthread_mutex_lock(&m1);
   pthread_mutex_lock(&m2);
   pthread_mutex_unlock(&m2);
   pthread_mutex_unlock(&m1);
   pthread_exit(0);
}

void* thread2(void* arg)
{
   pthread_mutex_lock(&m2);
   pthread_mutex_lock(&m1);
   pthread_mutex_unlock(&m1);
   pthread_mutex_unlock(&m2);
   pthread_exit(0);
}

int main()
{
   pthread_mutex_init(&m1, nullptr);
   pthread_mutex_init(&m2, nullptr);
   
   pthread_create(&thr1, 0, thread1, nullptr);
   pthread_create(&thr2, 0, thread2, nullptr);
   
   pthread_join(thr1, nullptr);
   pthread_join(thr2, nullptr);

   return 0;
}

//--------------------------------------------------------------------------------------------------
