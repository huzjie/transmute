// 最小 C++ 示例：一个计数器类
#include <cstdint>

class Counter {
 public:
  Counter() : count_(0) {}

  void increment() { count_++; }
  void decrement() { count_--; }
  int64_t value() const { return count_; }

 private:
  int64_t count_;
};
