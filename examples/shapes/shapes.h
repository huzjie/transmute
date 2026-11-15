#ifndef SHAPES_H
#define SHAPES_H

#include <cstdint>

struct Point {
  double x;
  double y;
};

class Shape {
 public:
  virtual ~Shape() {}
  virtual double area() const = 0;
  virtual double perimeter() const = 0;
};

class Circle : public Shape {
 public:
  explicit Circle(double radius);
  double area() const override;
  double perimeter() const override;

 private:
  double radius_;
};

class Rectangle : public Shape {
 public:
  Rectangle(double width, double height);
  double area() const override;
  double perimeter() const override;

 private:
  double width_;
  double height_;
};

#endif  // SHAPES_H
