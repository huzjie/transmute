#include "shapes.h"

#include <cassert>
#include <cmath>

int main() {
  Circle c(2.0);
  assert(std::fabs(c.area() - 4.0 * M_PI) < 1e-6);

  Rectangle r(3.0, 4.0);
  assert(r.area() == 12.0);
  assert(r.perimeter() == 14.0);
  return 0;
}
