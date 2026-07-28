#Task 5: Extending a Class
import math

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def distance(self, other):
        return math.sqrt(
            (other.x - self.x) ** 2 +
            (other.y - self.y) ** 2
        ) 
class Vector(Point):

        def __str__(self):
            return f"Vector({self.x}, {self.y})"    

        def __add__(self, other):
            return Vector(
                self.x + other.x,
                self.y + other.y

            )

p1 = Point(0, 0)
p2 = Point(3, 4)

print(p1)
print(p2)

print(p1 == Point(0, 0))

print(p1.distance(p2))

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1)
print(v2)

print(v1 + v2)