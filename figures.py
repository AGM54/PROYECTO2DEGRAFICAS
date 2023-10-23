from math import tan, pi, atan2, acos

class Intercept(object):
    def __init__(self, distance, point, normal, texcoords, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None

class Sphere(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        L = subtract(self.position, orig)
        lengthL = magnitude(L)
        tca = dot(L, dir)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        P = add(orig, multiply(dir, t0))

        normal = subtract(P, self.position)
        normal = normalize(normal)

        u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance=t0,
                         point=P,
                         normal=normal,
                         texcoords=(u, v),
                         obj=self)

# Vectores y operaciones
def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def add(v1, v2):
    return [x + y for x, y in zip(v1, v2)]

def subtract(v1, v2):
    return [x - y for x, y in zip(v1, v2)]

def multiply(v, scalar):
    return [x * scalar for x in v]

def magnitude(v):
    return (sum(x ** 2 for x in v)) ** 0.5

def normalize(v):
    mag = magnitude(v)
    return [x / mag for x in v]

class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = normalize(normal)
        super().__init__(position, material)

    def ray_intersect(self, origin, dir):
        denom = dot(dir, self.normal)
        if abs(denom) <= 0.0001:
            return None

        num = dot(subtract(self.position, origin), self.normal)
        t = num / denom
        if t < 0:
            return None

        P = add(origin, multiply(dir, t))
        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)

    def ray_intersect(self, origin, dir):
        planeIntersect = super().ray_intersect(origin, dir)
        if planeIntersect is None:
            return None

        contactDistance = subtract(planeIntersect.point, self.position)
        if magnitude(contactDistance) > self.radius:
            return None

        return Intercept(distance=planeIntersect.distance,
                         point=planeIntersect.point,
                         normal=self.normal,
                         texcoords=None,
                         obj=self)

class AABB(Shape):
    def __init__(self, position, size, material):
        super().__init__(position, material)
        self.planes = []
        self.size = size

        # Sides
        leftPlane = Plane(add(self.position, (-size[0] / 2, 0, 0)), (-1, 0, 0), material)
        rightPlane = Plane(add(self.position, (size[0] / 2, 0, 0)), (1, 0, 0), material)
        bottomPlane = Plane(add(self.position, (0, -size[1] / 2, 0)), (0, -1, 0), material)
        topPlane = Plane(add(self.position, (0, size[1] / 2, 0)), (0, 1, 0), material)
        backPlane = Plane(add(self.position, (0, 0, -size[2] / 2)), (0, 0, -1), material)
        frontPlane = Plane(add(self.position, (0, 0, size[2] / 2)), (0, 0, 1), material)
        
        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        # Bounds
        bias = 0.001
        self.boundsMin = [self.position[i] - (bias + size[i] / 2) for i in range(3)]
        self.boundsMax = [self.position[i] + (bias + size[i] / 2) for i in range(3)]

    def ray_intersect(self, orig, dir):
        intersect = None
        t = float("inf")
        u = 0
        v = 0

        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig, dir)
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0] and \
                   self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1] and \
                   self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                   
                    if planeIntersect.distance < t:
                        t = planeIntersect.distance
                        intersect = planeIntersect
                        
                        # Generate the UVs
                        if abs(plane.normal[0]) > 0:
                            # It's a left or right plane
                            u = (planePoint[1] - self.boundsMin[1]) / self.size[1]
                            v = (planePoint[2] - self.boundsMin[2]) / self.size[2]
                        elif abs(plane.normal[1]) > 0:
                            u = (planePoint[0] - self.boundsMin[0]) / self.size[0]
                            v = (planePoint[2] - self.boundsMin[2]) / self.size[2]
                        elif abs(plane.normal[2]) > 0:
                            u = (planePoint[0] - self.boundsMin[0]) / self.size[0]
                            v = (planePoint[1] - self.boundsMin[1]) / self.size[1]

        if intersect is None:
            return None

        return Intercept(distance=t,
                         point=intersect.point,
                         normal=intersect.normal,
                         texcoords=(u, v),
                         obj=self)

class Ellipsoid(Sphere):
    def __init__(self, position, radii, material):
        # radii es una tupla (a, b, c) que representa los semiejes del elipsoide
        self.radii = radii
        super().__init__(position, 1, material)  # La esfera base tiene radio 1

    def ray_intersect(self, orig, dir):
        # Escalamos el origen y la dirección del rayo
        scaled_orig = [orig[i] / self.radii[i] for i in range(3)]
        scaled_dir = [dir[i] / self.radii[i] for i in range(3)]
        scaled_dir = normalize(scaled_dir)

        # Realizamos la intersección con la esfera unitaria
        intersect = super().ray_intersect(scaled_orig, scaled_dir)
        if intersect is None:
            return None

        # Desescalamos el punto de intersección y la normal
        real_point = [intersect.point[i] * self.radii[i] for i in range(3)]
        scaled_normal = [intersect.normal[i] / self.radii[i] for i in range(3)]
        real_normal = normalize(scaled_normal)

        # Devolvemos el resultado
        return Intercept(distance=intersect.distance,
                         point=real_point,
                         normal=real_normal,
                         texcoords=intersect.texcoords,
                         obj=self)
class OBB(Shape):
    def __init__(self, position, size, rotation_matrix, material):
        super().__init__(position, material)
        self.size = size
        self.rotation = rotation_matrix
        self.inverse_rotation = self.matrix_inverse(self.rotation)

    def matrix_vector_multiply(self, matrix, vector):
        result = [sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3)]
        return result

    def matrix_inverse(self, matrix):
        determinant = matrix[0][0]*(matrix[1][1]*matrix[2][2] - matrix[1][2]*matrix[2][1]) - matrix[0][1]*(matrix[1][0]*matrix[2][2] - matrix[1][2]*matrix[2][0]) + matrix[0][2]*(matrix[1][0]*matrix[2][1] - matrix[1][1]*matrix[2][0])
        if determinant == 0:
            raise ValueError("Matrix is singular and cannot be inverted")

        inv_det = 1.0 / determinant

        adjoint = [
            [
                (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]),
                -(matrix[0][1] * matrix[2][2] - matrix[0][2] * matrix[2][1]),
                (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1])
            ],
            [
                -(matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]),
                (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]),
                -(matrix[0][0] * matrix[1][2] - matrix[1][0] * matrix[0][2])
            ],
            [
                (matrix[1][0] * matrix[2][1] - matrix[2][0] * matrix[1][1]),
                -(matrix[0][0] * matrix[2][1] - matrix[2][0] * matrix[0][1]),
                (matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1])
            ]
        ]

        return [[adjoint[i][j] * inv_det for j in range(3)] for i in range(3)]

    def ray_intersect(self, orig, dir):
        # Transformar el rayo al espacio del OBB usando la inversa de la rotación
        transformed_orig = subtract(self.matrix_vector_multiply(self.inverse_rotation, subtract(orig, self.position)), self.position)
        transformed_dir = self.matrix_vector_multiply(self.inverse_rotation, dir)

        # Bounds de la AABB (en espacio local del OBB)
        boundsMin = [-self.size[i] / 2 for i in range(3)]
        boundsMax = [self.size[i] / 2 for i in range(3)]

        # Comprobar intersección como si fuera un AABB en espacio local
        epsilon = 1e-8
        t_min = [(boundsMin[i] - transformed_orig[i]) / (transformed_dir[i] + epsilon) for i in range(3)]

      #  t_min = [(boundsMin[i] - transformed_orig[i]) / transformed_dir[i] for i in range(3)]
        epsilon = 1e-8
        t_max = [(boundsMax[i] - transformed_orig[i]) / (transformed_dir[i] + epsilon) for i in range(3)]


        t_near = max(min(t_min[0], t_max[0]), min(t_min[1], t_max[1]), min(t_min[2], t_max[2]))
        t_far = min(max(t_min[0], t_max[0]), max(t_min[1], t_max[1]), max(t_min[2], t_max[2]))

        if t_near > t_far or t_far < 0:
            return None

        t = t_near if t_near > 0 else t_far
        intersect_point = add(transformed_orig, multiply(transformed_dir, t))

        # Determinar la normal y las coordenadas UV.
        axis = max(enumerate([abs(intersect_point[0] - boundsMin[0]),
                              abs(intersect_point[1] - boundsMin[1]),
                              abs(intersect_point[2] - boundsMin[2])]), key=lambda x: x[1])[0]

        normal = [0, 0, 0]
        normal[axis] = 1 if intersect_point[axis] > 0 else -1

        u, v = 0, 0
        if axis == 0:
            u = (intersect_point[1] - boundsMin[1]) / self.size[1]
            v = (intersect_point[2] - boundsMin[2]) / self.size[2]
        elif axis == 1:
            u = (intersect_point[0] - boundsMin[0]) / self.size[0]
            v = (intersect_point[2] - boundsMin[2]) / self.size[2]
        elif axis == 2:
            u = (intersect_point[0] - boundsMin[0]) / self.size[0]
            v = (intersect_point[1] - boundsMin[1]) / self.size[1]

        # Transformar el punto de intersección y la normal de vuelta al espacio del mundo
        real_point = add(self.matrix_vector_multiply(self.rotation, intersect_point), self.position)
        real_normal = self.matrix_vector_multiply(self.rotation, normal)

        # Devolver el resultado
        return Intercept(distance=t,
                         point=real_point,
                         normal=real_normal,
                         texcoords=(u, v),
                         obj=self)
class ThinCylinder(Shape):
    def __init__(self, position, height, radius, material):
        super().__init__(position, material)
        self.height = height
        self.radius = radius

    def ray_intersect(self, orig, dir):
        # Transformamos el rayo al espacio del cilindro (centrado en el origen)
        transformed_orig = subtract(orig, self.position)

        a = dir[0]**2 + dir[2]**2
        b = 2 * (transformed_orig[0]*dir[0] + transformed_orig[2]*dir[2])
        c = transformed_orig[0]**2 + transformed_orig[2]**2 - self.radius**2

        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            return None

        if a == 0:
            if b != 0:
                t0 = -c/b
                t1 = -c/b
            else:
                return None
        else:
            t0 = (-b - discriminant**0.5) / (2*a)
            t1 = (-b + discriminant**0.5) / (2*a)

            if t0 > t1:
                t0, t1 = t1, t0

        y0 = transformed_orig[1] + t0 * dir[1]
        y1 = transformed_orig[1] + t1 * dir[1]

        if y0 < -self.height / 2:
            y0 = -self.height / 2
            t0 = (y0 - transformed_orig[1]) / dir[1]

        if y1 > self.height / 2:
            y1 = self.height / 2
            t1 = (y1 - transformed_orig[1]) / dir[1]

        if y0 > self.height / 2 or y1 < -self.height / 2 or t0 > t1:
            return None

        t = t0 if y0 > -self.height / 2 else t1

        if t < 0:
            return None

        P = add(orig, multiply(dir, t))
        normal = subtract(P, add(self.position, (0, P[1], 0)))
        normal = normalize(normal)

        return Intercept(distance=t,
                         point=P,
                         normal=normal,
                         texcoords=None,
                         obj=self)

class Line(object):
    def __init__(self, point, direction):
        self.point = point
        self.direction = normalize(direction)

    def get_point(self, t):
        """Get a point on the line for a given parameter t."""
        return add(self.point, multiply(self.direction, t))

    def __repr__(self):
        return f"Line(point={self.point}, direction={self.direction})"
class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        # Calculamos el centroide del triángulo para usarlo como posición
        position = [(v0[i] + v1[i] + v2[i]) / 3 for i in range(3)]
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        EPSILON = 1e-8
        edge1 = subtract(self.v1, self.v0)
        edge2 = subtract(self.v2, self.v0)
        h = cross(dir, edge2)
        a = dot(edge1, h)
        if -EPSILON < a < EPSILON:
            return None  # Rayo es paralelo al triángulo
        f = 1.0 / a
        s = subtract(orig, self.v0)
        u = f * dot(s, h)
        if u < 0.0 or u > 1.0:
            return None
        q = cross(s, edge1)
        v = f * dot(dir, q)
        if v < 0.0 or u + v > 1.0:
            return None
        t = f * dot(edge2, q)
        if t > EPSILON:
            intersection_point = add(orig, multiply(dir, t))
            normal = cross(edge1, edge2)  # La normal del triángulo
            normal = normalize(normal)
            return Intercept(distance=t,
                             point=intersection_point,
                             normal=normal,
                             texcoords=None,  # Puedes agregar cálculo de UV si lo necesitas
                             obj=self)
        return None

def cross(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]
