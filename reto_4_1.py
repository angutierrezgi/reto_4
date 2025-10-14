import math

class Point():
    definition: str = "Entidad geometrica abstracta que representa una ubicación en un espacio."
    def __init__(self, x: float=0, y: float=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, new_y):
        self._y = new_y
    
    def reset(self):
        self.x = 0
        self.y = 0
    def compute_distance(self, point: "Point")-> float:
        distance = ((self.x - point.x)**2+(self.y - point.y)**2)**(0.5)
        return distance
    def __repr__(self):
        return f"({self.x},{self.y})"
    
class Line():
    def __init__(self, start_point: Point, end_point: Point):
        self._start: Point = start_point
        self._end: Point = end_point
        self._length: float = start_point.compute_distance(end_point)
        self._slope: float = self.compute_slope()

    @property
    def start(self):
        return self._start
    @property
    def y(self):
        return self._y
    
    def compute_length(self) -> float:
        return self._length
    def compute_slope(self) -> float:
        slope: float = None
        if self._end.x - self._start.x == 0:
            slope = None
            return slope
        else:
            slope = (self._end.y - self._start.y) / (self._end.x - self._start.x)
            return round(slope, 3)
    def compute_horizontal_cross(self) -> bool:
        x_intersect: bool = False
        if self._start.y >= 0 and self._end.y <= 0:
            x_intersect = True
        elif self._start.y <= 0 and self._end.y >= 0:
            x_intersect = True
        return x_intersect
    def compute_vertical_cross(self) -> bool:
        y_intersect: bool = False
        if self._start.x >= 0 and self._end.x <= 0:
            y_intersect = True
        elif self._start.x <= 0 and self._end.x >= 0:
            y_intersect = True
        return y_intersect
    def discretize_line(self, n : int) -> list:
        i: int = 0
        points: list = []
        while(i < n):
            aux_x = self._start.x + ((i / (n - 1)) * (self._end.x - self._start.x))
            aux_y = self._start.y + ((i / (n - 1)) * (self._end.y - self._start.y))
            points.append(Point(round(aux_x, 3),round(aux_y, 3)))
            i += 1
        return points
    def __str__(self):
        result: list = [
            f"Start: {self._start}",
            f"End: {self._end}",
            f"Length: {self.compute_length()}",
            f"Slope: {self.compute_slope()}",
            f"Cross x-axis: {self.compute_horizontal_cross()}",
            f"Cross y-axis: {self.compute_vertical_cross()}"
        ]
        return "\n".join(result)

class Shape():
    def __init__(self, vertices: list, edges: list):
        self._vertices: list = vertices
        self._edges: list = edges
        self._inner_angles: list = self.compute_inner_angles()
        self.is_regular: bool = False
    def compute_inner_angles(self) -> list:
        angles: list = []
        n_verts = len(self._vertices)
        for i in range(n_verts):
            prev_vert = self._vertices[i - 1]
            midl_vert = self._vertices[i]
            next_vert = self._vertices[(i + 1) % n_verts]

            v = [prev_vert.x - midl_vert.x, prev_vert.y - midl_vert.y]
            u = [next_vert.x - midl_vert.x, next_vert.y - midl_vert.y]

            dot_prod = v[0] * u[0] + v[1] * u[1]
            norm_v = ((v[0] * v[0]) + (v[1] * v[1])) ** 0.5
            norm_u = ((u[0] * u[0]) + (u[1] * u[1])) ** 0.5

            cos_angle = dot_prod / (norm_u * norm_v)
            cos_angle = max(-1.0, min(1.0, cos_angle))
            angle_rad = math.acos(cos_angle)
            angle_deg = math.degrees(angle_rad)

            angles.append(round(angle_deg, 3))
        return angles
    def compute_area():
        raise NotImplementedError("Must be implemented in subclass!!")
    def compute_perimeter():
        raise NotImplementedError("Must be implemented in subclass!!")

class Rectangle(Shape):
    def __init__(self, vertices: list, edges: list):
        super().__init__(vertices, edges)
        self.width: float = self._edges[0].compute_length()
        self.height: float = self._edges[1].compute_length()
        if self.width == self.height:
            self.is_regular: bool = True
        else:
            self.is_regular: bool = False
    def compute_area(self) -> float:
        return self.width * self.height
    def compute_perimeter(self) -> float:
        return 2*self.width + 2*self.height
    def __str__(self):
        result: list = [
            f"Vertices: {self._vertices}",
            f"Inner Angles: {self._inner_angles}",
            f"Width: {self.width}",
            f"Height: {self.height}",
            f"Regular Shape: {self.is_regular}",
            f"Area: {self.compute_area()}",
            f"Perimeter: {self.compute_perimeter()}"
        ]
        return "\n".join(result)  
      
class Square(Rectangle):
    def __init__(self, vertices: list, edges: list):
        super().__init__(vertices, edges)
        if not (self._edges[0].compute_length() == self._edges[1].compute_length()):
            raise ValueError("Not a Square")
        self.side_length: float = self._edges[0].compute_length()
        self.is_regular: bool = True
    def compute_area(self) -> float:
        return self.side_length ** 2
    def compute_perimeter(self) -> float:
        return 4 * self.side_length
    def __str__(self):
        result: list = [
            f"Vertices: {self._vertices}",
            f"Inner Angles: {self._inner_angles}",
            f"Side Length: {self.side_length}",
            f"Regular Shape: {self.is_regular}",
            f"Area: {self.compute_area()}",
            f"Perimeter: {self.compute_perimeter()}"
        ]
        return "\n".join(result)  
    
class Triangle(Shape):
    def __init__(self, vertices: list, edges: list):
        super().__init__(vertices, edges)
        self._a: float = self._edges[0].compute_length()
        self._b: float = self._edges[1].compute_length()
        self._c: float = self._edges[2].compute_length()
        if math.isclose(self._a, self._b) and math.isclose(self._b, self._c):
            self.is_regular: bool = True
        else:
            self.is_regular: bool = False
    def compute_perimeter(self):
        perimeter: float = self._a + self._b + self._c
        return round(perimeter, 3)
    def compute_area(self) -> float:
        s: float = self.compute_perimeter() / 2
        area : float = (s * (s - self._a) * (s - self._b) * (s - self._c)) ** 0.5
        return round(area, 3)
    def __str__(self):
        result: list = [
            f"Vertices: {self._vertices}",
            f"Inner Angles: {self._inner_angles}",
            f"Regular Shape: {self.is_regular}",
            f"Area: {self.compute_area()}",
            f"Perimeter: {self.compute_perimeter()}"
        ]
        return "\n".join(result)  
    
class Isosceles(Triangle):
    def __init__(self, vertices: list, edges: list):
        super().__init__(vertices, edges)
        if not (math.isclose(self._a, self._b) or math.isclose(self._b, self._c) or math.isclose(self._a, self._c)):
            raise ValueError("Not an Isosceles triangle!!")
    def compute_perimeter(self):
        return super().compute_perimeter()
    def compute_area(self):
        return super().compute_area()
    def __str__(self):
        return super().__str__()
    
class Equilateral(Triangle):
    def __init__(self, vertices: list, edges: list):
        super().__init__(vertices, edges)
        self.is_regular: bool = True
        if not (math.isclose(self._a, self._b) and math.isclose(self._b, self._c)):
            raise ValueError("Not an Equilateral triangle!!")
    def compute_perimeter(self):
        return super().compute_perimeter()
    def compute_area(self):
        return super().compute_area()
    def __str__(self):
        return super().__str__()
    
class Scalene(Triangle):
    def __init__(self, vertices: list, edges: list):
        super().__init__(vertices, edges)
        if math.isclose(self._a, self._b) or math.isclose(self._b, self._c) or math.isclose(self._a, self._c):
            raise ValueError("Not an Scalene triangle!!")
    def compute_perimeter(self):
        return super().compute_perimeter()
    def compute_area(self):
        return super().compute_area()
    def __str__(self):
        return super().__str__()
    
class TriRectangle(Triangle):
    def __init__(self, vertices:list, edges: list):
        super().__init__(vertices, edges)
        if not any(math.isclose(angle, 90.0) for angle in self._inner_angles):
            raise ValueError("Not a Right Triangle!!")
    def compute_perimeter(self):
        return super().compute_perimeter()
    def compute_area(self):
        return super().compute_area()
    def __str__(self):
        return super().__str__()

if __name__ == "__main__":
    
    # Test Rectangle (_vertices in order: bottom-left, bottom-right, top-right, top-left)
    rect_points = [Point(0,0), Point(4,0), Point(4,2), Point(0,2)]
    rect_lines = [
        Line(rect_points[0], rect_points[1]),
        Line(rect_points[1], rect_points[2]),
        Line(rect_points[2], rect_points[3]),
        Line(rect_points[3], rect_points[0])
    ]
    rectangle = Rectangle(rect_points, rect_lines)
    print("\nRectangle object:")
    print(rectangle)

    # Test Square
    square_points = [Point(1,1), Point(4,1), Point(4,4), Point(1,4)]
    square_lines = [
        Line(square_points[0], square_points[1]),
        Line(square_points[1], square_points[2]),
        Line(square_points[2], square_points[3]),
        Line(square_points[3], square_points[0])
    ]
    square = Square(square_points, square_lines)
    print("\nSquare Object:")
    print(square)

    # Test Triangle (vertices in order: A, B, C)
    tri_points = [Point(0, 0), Point(4, 0), Point(2, 3)]
    tri_lines = [
        Line(tri_points[0], tri_points[1]),
        Line(tri_points[1], tri_points[2]),
        Line(tri_points[2], tri_points[0])
    ]
    triangle = Triangle(tri_points, tri_lines)
    print("\nTriangle Object:")
    print(triangle)

    # Test Isosceles Triangle
    iso_points = [Point(0, 0), Point(2, 0), Point(1, 2)]
    iso_lines = [
        Line(iso_points[0], iso_points[1]),
        Line(iso_points[1], iso_points[2]),
        Line(iso_points[2], iso_points[0])
    ]
    isosceles = Isosceles(iso_points, iso_lines)
    print("\nIsosceles Object:")
    print(isosceles)
    
    # Test Equilateral Triangle
    eq_points = [Point(0, 0), Point(1, 0), Point(0.5, math.sqrt(3)/2)]
    eq_lines = [
        Line(eq_points[0], eq_points[1]),
        Line(eq_points[1], eq_points[2]),
        Line(eq_points[2], eq_points[0])
    ]
    equilateral = Equilateral(eq_points, eq_lines)
    print("\nEquilateral Object:")
    print(equilateral)

    # Test Scalene Triangle
    sca_points = [Point(0, 0), Point(4, 0), Point(3, 5)]
    sca_lines = [
        Line(sca_points[0], sca_points[1]),
        Line(sca_points[1], sca_points[2]),
        Line(sca_points[2], sca_points[0])
    ]
    scalene = Scalene(sca_points, sca_lines)
    print("\nScalene Object:")
    print(scalene)

    # Test Right Triangle (TriRectangle)
    right_points = [Point(0, 0), Point(3, 0), Point(0, 4)]
    right_lines = [
        Line(right_points[0], right_points[1]),
        Line(right_points[1], right_points[2]),
        Line(right_points[2], right_points[0])
    ]
    right_triangle = TriRectangle(right_points, right_lines)
    print("\nRight Triangle Object:")
    print(right_triangle)
