from math import pi, atan2
from functools import reduce
from operator import add
from common.r3 import R3


class Segment:
    """Одномерный отрезок"""

    # Параметры конструктора: начало и конец отрезка (числа)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin

    # Отрезок вырожден?
    def is_degenerate(self):
        return self.beg >= self.fin

    # Пересечение с отрезком
    def intersect(self, other):
        if other.beg > self.beg:
            self.beg = other.beg
        if other.fin < self.fin:
            self.fin = other.fin
        return self

    # Разность отрезков
    # Разность двух отрезков всегда является списком из двух отрезков!
    def subtraction(self, other):
        return [
            Segment(self.beg, self.fin if self.fin < other.beg else other.beg),
            Segment(self.beg if self.beg > other.fin else other.fin, self.fin),
        ]

    def __repr__(self):
        return f"{self.beg}, {self.fin}"


class Edge:
    """Ребро полиэдра"""

    # Начало и конец стандартного одномерного отрезка
    SBEG, SFIN = 0.0, 1.0

    # Параметры конструктора: начало и конец ребра (точки в R3)
    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin
        # Список «просветов»
        self.gaps = [Segment(Edge.SBEG, Edge.SFIN)]
        self.shade = [Segment(Edge.SFIN, Edge.SBEG)]

    # Учёт тени от одной грани
    def shadow(self, facet):
        # «Вертикальная» грань не затеняет ничего
        if facet.is_vertical():
            return
        # Нахождение одномерной тени на ребре
        shade = Segment(Edge.SBEG, Edge.SFIN)
        for u, v in zip(facet.vertexes, facet.v_normals()):
            shade.intersect(self.intersect_edge_with_normal(u, v))
            if shade.is_degenerate():
                return

        shade.intersect(
            self.intersect_edge_with_normal(facet.vertexes[0],
                                            facet.h_normal()))

        if shade.is_degenerate():
            return
        # Преобразование списка «просветов», если тень невырождена
        gaps = [s.subtraction(shade) for s in self.gaps]
        self.gaps = [s for s in reduce(add, gaps, []) if not s.is_degenerate()]

    def subtract_gaps_from_full(self):
        full = [Segment(0.0, 1.0)]
        for gap in self.gaps:
            new_full = []
            for seg in full:
                new_full.extend(seg.subtraction(gap))
            full = [s for s in new_full if not s.is_degenerate()]
        return full

    # Преобразование одномерных координат в трёхмерные
    def r3(self, t):
        return self.beg * (Edge.SFIN - t) + self.fin * t

    # Пересечение ребра с полупространством, задаваемым точкой (a)
    # на плоскости и вектором внешней нормали (n) к ней
    def intersect_edge_with_normal(self, a, n):
        f0, f1 = n.dot(self.beg - a), n.dot(self.fin - a)
        if f0 >= 0.0 and f1 >= 0.0:
            return Segment(Edge.SFIN, Edge.SBEG)
        if f0 < 0.0 and f1 < 0.0:
            return Segment(Edge.SBEG, Edge.SFIN)
        x = -f0 / (f1 - f0)
        return Segment(Edge.SBEG, x) if f0 < 0.0 else Segment(x, Edge.SFIN)


class Facet:
    """Грань полиэдра"""

    # Параметры конструктора: список вершин

    def __init__(self, vertexes):
        self.vertexes = vertexes
        self.area = self._area(Polyedr.scale)
        self.good_vertices_count = sum(
            1 for v in self.vertexes if v.is_good_point(
                Polyedr.alpha, Polyedr.beta, Polyedr.gamma, Polyedr.scale))

    # Возвращает True, если не более 2 вершин грани - "хорошие"
    def qualifies_for_special_area(self):
        return self.good_vertices_count <= 2

    # Возвращает площадь, если грань удовлетворяет условию
    def get_special_area(self):
        return self.area if self.qualifies_for_special_area() else 0.0

    def _area(self, c=1.0, to_calculate=True):
        n = len(self.vertexes)
        s = 0.0
        if n <= 2:
            to_calculate = False
        if to_calculate:
            mean = self.center()
            s = 0.0
            for i in range(n):
                a1 = self.vertexes[i - 1] - mean
                a2 = self.vertexes[i] - mean
                s += a1.cross(a2).length()
            s *= 0.5 / c**2
        return s

    # «Вертикальна» ли грань?
    def is_vertical(self):
        return self.h_normal().dot(Polyedr.V) == 0.0

    # Нормаль к «горизонтальному» полупространству
    def h_normal(self):
        n = (self.vertexes[1] - self.vertexes[0]).cross(self.vertexes[2] -
                                                        self.vertexes[0])
        return n * (-1.0) if n.dot(Polyedr.V) < 0.0 else n

    # Нормали к «вертикальным» полупространствам, причём k-я из них
    # является нормалью к грани, которая содержит ребро, соединяющее
    # вершины с индексами k-1 и k
    def v_normals(self):
        return [self._vert(x) for x in range(len(self.vertexes))]

    # Вспомогательный метод
    def _vert(self, k):
        n = (self.vertexes[k] - self.vertexes[k - 1]).cross(Polyedr.V)
        return (n * (-1.0) if n.dot(self.vertexes[k - 1] -
                                    self.center()) < 0.0 else n)

    # Центр грани
    def center(self):
        return sum(self.vertexes, R3(0.0, 0.0,
                                     0.0)) * (1.0 / len(self.vertexes))


class Polyedr:
    """Полиэдр"""

    # вектор проектирования
    V = R3(0.0, 0.0, 1.0)
    scale = 1.0

    # Параметры конструктора: файл, задающий полиэдр
    def __init__(self, file):
        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.edges, self.facets = [], [], []

        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    c = float(buf.pop(0))
                    Polyedr.scale = c
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                    Polyedr.alpha, Polyedr.beta, Polyedr.gamma = (
                        alpha,
                        beta,
                        gamma,
                    )
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    self.vertexes.append(
                        R3(x, y, z).rz(alpha).ry(beta).rz(gamma) * c)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = list(self.vertexes[int(n) - 1] for n in buf)
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    def calculate_special_area(self):
        return sum(f.get_special_area() for f in self.facets)

    # Метод изображения полиэдра
    def draw(self, tk):  # pragma: no cover
        tk.clean()
        tk.draw_axes(Polyedr.alpha, Polyedr.beta, Polyedr.gamma, Polyedr.scale)
        tk.draw_plane(Polyedr.alpha, Polyedr.beta, Polyedr.gamma,
                      Polyedr.scale)
        for e in self.edges:
            a1, a2 = e.beg, e.fin
            tk.draw_point(a1, Polyedr.alpha, Polyedr.beta, Polyedr.gamma,
                          Polyedr.scale)
            tk.draw_point(a2, Polyedr.alpha, Polyedr.beta, Polyedr.gamma,
                          Polyedr.scale)
            for f in self.facets:
                e.shadow(f)
            for s in e.gaps:
                tk.draw_line(e.r3(s.beg), e.r3(s.fin))
            shades = e.subtract_gaps_from_full()
            for s in shades:
                tk.draw_line(e.r3(s.beg), e.r3(s.fin), dash=(10, 25))
