#ifndef COUNTER_H
#define COUNTER_H

#include <cstdint>

class Counter {
 public:
  Counter();
  void increment();
  void decrement();
  int64_t value() const;

 private:
  int64_t count_;
};

#endif  // COUNTER_H
