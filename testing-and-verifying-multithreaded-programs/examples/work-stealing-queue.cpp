
//-----------------------------------------------------------------------------------------------100
/// @file work-stealing-queue.cpp
/// @author Susanne van den Elsen
/// @date 2017
//--------------------------------------------------------------------------------------------------

#include <array>
#include <atomic>
#include <thread>

#define SIZE 1

//--------------------------------------------------------------------------------------------------

class work_stealing_queue
{
public:

   work_stealing_queue() : m_jobs({}), m_head(0), m_tail(0), m_mask(SIZE-1)
   {
   }

   void push(const int job)
   {
     unsigned int tail = m_tail.load();
     unsigned int head = m_head.load();

//      if (m_tail < m_mask) // && tail < max_size    // CORRECT
      if (tail < head+SIZE)  // && tail < max_size     // DATARACE
      {
         m_jobs[tail & m_mask] = job;
         m_tail.store(tail+1);
      }
   }

   int steal()
   {
      unsigned int head = m_head.load();
      m_head.store(head+1);

      if (head < m_tail)
      {
         int job = m_jobs[head & m_mask];
         return job;
      }
      return -1;
   }

private:

   std::array<int,SIZE> m_jobs;
   std::atomic<unsigned int> m_head;
   std::atomic<unsigned int> m_tail;

   size_t m_mask;

}; // end class work_stealing_queue

//--------------------------------------------------------------------------------------------------

void master_thread(work_stealing_queue& queue)
{
   for (int i = 0; i < 2; ++i)
   {
      queue.push(i);
   }
   pthread_exit(0);
}

//--------------------------------------------------------------------------------------------------

void worker_thread(work_stealing_queue& queue)
{
   for (int i = 0; i < 1; ++i)
   {
      int job = queue.steal();
   }
   pthread_exit(0);
}

//--------------------------------------------------------------------------------------------------

int main()
{
   work_stealing_queue queue;
   
   std::thread master(master_thread, std::ref(queue));
   std::thread worker1(worker_thread, std::ref(queue));
   
   master.join();
   worker1.join();
   
   return 0;
}

//--------------------------------------------------------------------------------------------------
