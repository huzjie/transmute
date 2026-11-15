#include "counter.h"
#include <cassert>

int main() {
  Counter c;
  assert(c.value() == 0);
  c.increment();
  c.increment();
  assert(c.value() == 2);
  c.decrement();
  assert(c.value() == 1);
  return 0;
}
