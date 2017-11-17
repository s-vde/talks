
//-----------------------------------------------------------------------------------------------100
/// @file lock_free_queue.cpp
/// @author Susanne van den Elsen
/// @date 2017
//--------------------------------------------------------------------------------------------------

#include <array>
#include <atomic>
#include <thread>


//--------------------------------------------------------------------------------------------------

class lock_free_queue
{
public:
   lock_free_queue();

   void push(const int job);
   int steal();

private:
   std::array<int, SIZE> m_jobs;
   std::atomic<size_t> m_head;
   std::atomic<size_t> m_tail;

}; // end class lock_free_queue

//--------------------------------------------------------------------------------------------------

lock_free_queue::lock_free_queue()
: m_jobs({})
, m_head(0)
, m_tail(0)
{
}

//--------------------------------------------------------------------------------------------------

void lock_free_queue::push(const int job)
{
   const size_t tail = m_tail.load();

   // if (tail < m_head.load() + SIZE - 1) // CORRECT
   if (tail < m_head.load() + SIZE) // BUG
   {
      m_jobs[tail % SIZE] = job;
      m_tail.store(tail + 1);
   }
}

//--------------------------------------------------------------------------------------------------

int lock_free_queue::steal()
{
   size_t head = m_head.load();

   if (head < m_tail.load())
   {
      // in the meanwhile, m_tail may have been incremented, but this is not a problem since 
      // head < m_tail will still hold

      if (m_head.compare_exchange_strong(head, head + 1))
      {
         return m_jobs[head % SIZE];
      }

      // else: another thread has updated m_head in the meanwhile
   }
   // else: queue empty
   
   return -1;
}

//--------------------------------------------------------------------------------------------------
