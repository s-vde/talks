
//--------------------------------------------------------------------------------------------------
/// @file simple_data_race.cpp
//--------------------------------------------------------------------------------------------------

#include <pthread.h>

int x = 0;
pthread_t thread1, thread2;
int values[2] = {0, 1};

pthread_mutex_t mutex;

void* thread_routine(void* arg)
{
   int value = *(int*) arg;
   
   pthread_mutex_lock(&mutex);
   x = value;
   pthread_mutex_unlock(&mutex);
   pthread_exit(0);
}

int main()
{
   pthread_mutex_init(&mutex, NULL);
   
   pthread_create(&thread1, 0, thread_routine, values + 0);
   pthread_create(&thread2, 0, thread_routine, values + 1);
   
   pthread_join(thread1, NULL);
   pthread_join(thread2, NULL);

   return 0;
}
