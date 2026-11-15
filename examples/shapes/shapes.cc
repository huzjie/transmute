#include "shapes.h"

#include <cmath>

Circle::Circle(double radius) : radius_(radius) {}

double Circle::area() const { return M_PI * radius_ * radius_; }

double Circle::perimeter() const { return 2.0 * M_PI * radius_; }

Rectangle::Rectangle(double width, double height)
    : width_(width), height_(height) {}

double Rectangle::area() const { return width_ * height_; }

double Rectangle::perimeter() const { return 2.0 * (width_ + height_); }
