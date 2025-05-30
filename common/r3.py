from math import sin, cos, sqrt


class R3:
    """Вектор (точка) в R3"""

    # Конструктор
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    # Сумма векторов
    def __add__(self, other):
        return R3(self.x + other.x, self.y + other.y, self.z + other.z)

    # Разность векторов
    def __sub__(self, other):
        return R3(self.x - other.x, self.y - other.y, self.z - other.z)

    # Умножение на число
    def __mul__(self, k):
        return R3(k * self.x, k * self.y, k * self.z)

    # Поворот вокруг оси Oz
    def rz(self, fi):
        return R3(
            cos(fi) * self.x - sin(fi) * self.y,
            sin(fi) * self.x + cos(fi) * self.y,
            self.z,
        )

    # Поворот вокруг оси Oy
    def ry(self, fi):
        return R3(
            cos(fi) * self.x + sin(fi) * self.z,
            self.y,
            -sin(fi) * self.x + cos(fi) * self.z,
        )

    # Скалярное произведение
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # Векторное произведение
    def cross(self, other):
        return R3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def transform(self, alpha, beta, gamma, c=1.0):
        return self.rz(alpha).ry(beta).rz(gamma) * c

    def untransform(self, alpha, beta, gamma, c=1.0):
        return self.rz(-gamma).ry(-beta).rz(-alpha) * (1 / c)

    def distance_to_plane(self, alpha, beta, gamma, c, value=-1.0, axis="y"):
        distance = 0.0
        self = self.untransform(alpha, beta, gamma, c)
        if axis == "x":
            distance = abs(self.x - value)
        elif axis == "y":
            distance = abs(self.y - value)
        elif axis == "z":
            distance = abs(self.z - value)
        else:
            raise ValueError("Недопустимая ось. Используйте 'x', 'y' или 'z'")
        return distance

    # Для задания
    def is_good_point(self, alpha, beta, gamma, c=1.0, distance=1.0):
        #print(self.distance_to_plane(alpha, beta, gamma, c) > distance)
        return self.distance_to_plane(alpha, beta, gamma, c) > distance

    # Длина вектора
    def length(self):
        return sqrt(self.dot(self))

    def __eq__(self, other):
        if not isinstance(other, R3):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f"{(self.x, self.y, self.z)}"


if __name__ == "__main__":  # pragma: no cover
    x = R3(1.0, 34.0, 354.0)
    alpha, beta, gamma, c = 20, 40, 69, 349
    x = x.transform(alpha, beta, gamma, c)
    x = x.untransform(alpha, beta, gamma, c)
    print(x)
