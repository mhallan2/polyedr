import unittest
from math import sqrt, isclose
from common.r3 import R3
from shadow.polyedr import Facet
from tests.matchers import R3ApproxMatcher, R3CollinearMatcher


class TestVoid(unittest.TestCase):

    # Эта грань не является вертикальной
    def test_vertical01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        self.assertFalse(f.is_vertical())

    # Эта грань вертикальна
    def test_vertical02(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(0.0, 0.0, 1.0), R3(1.0, 0.0, 0.0)])
        self.assertTrue(f.is_vertical())

    # Нормаль к этой грани направлена вертикально вверх
    def test_h_normal01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        self.assertEqual(R3CollinearMatcher(f.h_normal()), R3(0.0, 0.0, 1.0))

    # Нормаль к этой грани тоже направлена вертикально вверх
    def test_h_normal02(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(0.0, 3.0, 0.0), R3(3.0, 0.0, 0.0)])
        self.assertEqual(R3CollinearMatcher(f.h_normal()), R3(0.0, 0.0, 1.0))

    # Для нахождения нормали к этой грани рекомендуется нарисовать картинку
    def test_h_normal03(self):
        f = Facet([R3(1.0, 0.0, 0.0), R3(0.0, 1.0, 0.0), R3(0.0, 0.0, 1.0)])
        self.assertEqual(R3CollinearMatcher(f.h_normal()), R3(1.0, 1.0, 1.0))

    # Для каждой из следующих граней сначала «вручную» находятся
    # внешние нормали к вертикальным плоскостям, проходящим через
    # рёбра заданной грани, а затем проверяется, что эти нормали
    # имеют то же направление, что и вычисляемые методом v_normals

    # Нормали для треугольной грани
    def test_v_normal01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        normals = [R3(-1.0, 0.0, 0.0), R3(0.0, -1.0, 0.0), R3(1.0, 1.0, 0.0)]
        for t in zip(f.v_normals(), normals):
            self.assertEqual(R3CollinearMatcher(t[0]), t[1])

    # Нормали для квадратной грани
    def test_v_normal02(self):
        f = Facet([
            R3(0.0, 0.0, 0.0),
            R3(2.0, 0.0, 0.0),
            R3(2.0, 2.0, 0.0),
            R3(0.0, 2.0, 0.0)
        ])
        normals = [
            R3(-1.0, 0.0, 0.0),
            R3(0.0, -1.0, 0.0),
            R3(1.0, 0.0, 0.0),
            R3(0.0, 1.0, 0.0)
        ]
        for t in zip(f.v_normals(), normals):
            self.assertEqual(R3CollinearMatcher(t[0]), t[1])

    # Нормали для ещё одной треугольной грани
    def test_v_normal03(self):
        f = Facet([R3(1.0, 0.0, 0.0), R3(0.0, 1.0, 0.0), R3(0.0, 0.0, 1.0)])
        normals = [R3(0.0, -1.0, 0.0), R3(1.0, 1.0, 0.0), R3(-1.0, 0.0, 0.0)]
        for t in zip(f.v_normals(), normals):
            self.assertEqual(R3CollinearMatcher(t[0]), t[1])

    # Центр квадрата
    def test_center01(self):
        f = Facet([
            R3(0.0, 0.0, 0.0),
            R3(2.0, 0.0, 0.0),
            R3(2.0, 2.0, 0.0),
            R3(0.0, 2.0, 0.0)
        ])
        self.assertEqual(R3ApproxMatcher(f.center()), (R3(1.0, 1.0, 0.0)))

    # Центр треугольника
    def test_center02(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(3.0, 0.0, 0.0), R3(0.0, 3.0, 0.0)])
        self.assertEqual(R3ApproxMatcher(f.center()), (R3(1.0, 1.0, 0.0)))

    # Тест площади треугольника (проекция на XY)
    def test_calculate_area01(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(2.0, 0.0, 0.0), R3(0.0, 2.0, 0.0)])
        self.assertTrue(isclose(f._area(), 2.0))

    # Тест площади квадрата (проекция на XZ)
    def test_calculate_area02(self):
        f = Facet([
            R3(0.0, 0.0, 0.0),
            R3(2.0, 0.0, 0.0),
            R3(2.0, 0.0, 2.0),
            R3(0.0, 0.0, 2.0)
        ])
        self.assertTrue(isclose(f._area(), 4.0))

    # Тест площади вырожденной грани
    def test_calculate_area03(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(1.0, 0.0, 0.0)])
        self.assertTrue(isclose(f._area(), 0.0))

    # Тест площади треугольника (проекция на YZ)
    def test_calculate_area04(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(0.0, 3.0, 0.0), R3(0.0, 0.0, 3.0)])
        self.assertTrue(isclose(f._area(), 4.5))

    # Тест условия на "хорошие" вершины (<= 2)
    def test_qualifies_for_special_area_true(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(0.0, 2.0, 2.0), R3(0.0, 2.0, 0.0)])
        # Вручную указываем количество "хороших" вершин, как будто бы
        # коэффициент гомотетии полиэдра равен 1.
        f.good_vertices_count = 2
        self.assertTrue(f.qualifies_for_special_area())

    # Тест условия на "хорошие" вершины (> 2)
    def test_qualifies_for_special_area_false(self):
        f = Facet([
            R3(0.0, 0.0, 0.0),
            R3(0.0, 2.0, 2.0),
            R3(0.0, 2.0, 0.0),
            R3(0.0, 3.0, 1.0)
        ])
        # Заглушка для теста
        f.good_vertices_count = 3
        self.assertFalse(f.qualifies_for_special_area())

    # Тест возврата площади для подходящей грани
    def test_get_special_area_qualified(self):
        f = Facet([R3(0.0, 0.0, 0.0), R3(2.0, 0.0, 0.0), R3(0.0, 2.0, 0.0)])
        f.area = f._area()
        f.good_vertices_count = 1
        self.assertTrue(isclose(f.get_special_area(), f.area))

    # Тест возврата 0 для неподходящей грани
    def test_get_special_area_not_qualified(self):
        f = Facet([
            R3(0.0, 0.0, 0.0),
            R3(0.0, 2.0, 2.0),
            R3(0.0, 2.0, 0.0),
            R3(0.0, 3.0, 1.0)
        ])
        f.good_vertices_count = 3
        self.assertTrue(isclose(f.get_special_area(), 0.0))
