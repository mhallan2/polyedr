import unittest

from math import pi
from common.r3 import R3
from tests.matchers import R3ApproxMatcher


class TestR3(unittest.TestCase):

    def setUp(self):
        self.a = R3(1.0, 2.0, 3.0)

    def test_add01(self):
        self.assertIsInstance(self.a + R3(0.0, 0.0, 0.0), R3)

    def test_add02(self):
        self.assertEqual(R3ApproxMatcher(self.a + R3(0.0, 0.0, 0.0)), self.a)

    def test_add03(self):
        self.assertEqual(R3ApproxMatcher(self.a + R3(0.0, 1.0, 2.0)),
                         R3(1.0, 3.0, 5.0))

    def test_add04(self):
        self.assertEqual(R3ApproxMatcher(self.a + R3(-1.0, -2.0, -3.0)),
                         R3(0.0, 0.0, 0.0))

    def test_sub01(self):
        self.assertIsInstance(self.a - R3(0.0, 0.0, 0.0), R3)

    def test_sub02(self):
        self.assertEqual(R3ApproxMatcher(self.a - R3(0.0, 0.0, 0.0)), self.a)

    def test_sub03(self):
        self.assertEqual(R3ApproxMatcher(self.a - R3(0.0, 1.0, 2.0)),
                         R3(1.0, 1.0, 1.0))

    def test_sub04(self):
        self.assertEqual(R3ApproxMatcher(self.a - self.a), R3(0.0, 0.0, 0.0))

    def test_mul01(self):
        self.assertIsInstance(self.a * 3, R3)

    def test_mul02(self):
        self.assertEqual(R3ApproxMatcher(self.a * 1), self.a)

    def test_mul03(self):
        self.assertEqual(R3ApproxMatcher(self.a * 3.0),
                         R3(3.0, 6.0, 9.0))

    def test_mul04(self):
        self.assertEqual(R3ApproxMatcher(self.a + self.a), self.a * 2)

    def test_rz01(self):
        self.assertIsInstance(self.a.rz(45.0), R3)

    def test_rz02(self):
        self.assertEqual(R3ApproxMatcher(self.a.rz(0.0)), self.a)

    def test_rz03(self):
        self.assertEqual(R3ApproxMatcher(self.a.rz(pi)),
                         R3(-self.a.x, -self.a.y, self.a.z))

    def test_rz04(self):
        self.assertEqual(R3ApproxMatcher(self.a.rz(2 * pi)), self.a)

    def test_ry01(self):
        self.assertIsInstance(self.a.ry(45.0), R3)

    def test_ry02(self):
        self.assertEqual(R3ApproxMatcher(self.a.ry(0.0)), self.a)

    def test_ry03(self):
        self.assertEqual(R3ApproxMatcher(self.a.ry(pi)),
                         R3(-self.a.x, self.a.y, -self.a.z))

    def test_ry04(self):
        self.assertEqual(R3ApproxMatcher(self.a.ry(2 * pi)), self.a)

    def test_dot01(self):
        self.assertIsInstance(self.a.dot(self.a), float)

    def test_dot02(self):
        self.assertEqual(self.a.dot(R3(0.0, 0.0, 0.0)), 0.0)

    def test_dot03(self):
        b = R3(3.0, 2.0, 1.0)
        self.assertAlmostEqual(self.a.dot(b), 10.0)

    def test_dot04(self):
        b = R3(-3.0, -2.0, -1.0)
        self.assertAlmostEqual(self.a.dot(b), b.dot(self.a))

    def test_dot05(self):
        b = R3(1.0, -2.0, 1.0)
        self.assertAlmostEqual(self.a.dot(b), 0.0)

    def test_cross01(self):
        self.assertIsInstance(self.a.cross(self.a), R3)

    def test_cross02(self):
        self.assertEqual(R3ApproxMatcher(self.a.cross(R3(0.0, 0.0, 0.0))),
                         R3(0.0, 0.0, 0.0))

    def test_cross03(self):
        self.assertEqual(R3ApproxMatcher(self.a.cross(self.a)),
                         R3(0.0, 0.0, 0.0))

    def test_cross04(self):
        self.assertEqual(R3ApproxMatcher(self.a.cross(R3(3.0, -2.0, 1.0))),
                         R3(8.0, 8.0, -8.0))

    # Тесты расстояний до разных плоскостей
    def test_distance_to_plane01(self):
        point = R3(-2.0, 0.0, 0.0)
        self.assertAlmostEqual(point.distance_to_plane(1.0, -1.0, 'x'), 1.0)

    def test_distance_to_plane02(self):
        point = R3(0.0, 2.0, 0.0)
        self.assertAlmostEqual(point.distance_to_plane(1.0, 1.0, 'y'), 1.0)

    def test_distance_to_plane03(self):
        point = R3(0.0, 0.0, 2.0)
        self.assertAlmostEqual(point.distance_to_plane(1.0, 1.0, 'z'), 1.0)

    # Неверно выбранная ось (плоскость)
    def test_distance_to_plane04(self):
        with self.assertRaises(ValueError):
            self.a.distance_to_plane(1.0, 1.0, 'invalid')

    # Расстояние равно 0
    def test_distance_to_plane05(self):
        point = R3(1.0, 0.0, 0.0)
        self.assertAlmostEqual(point.distance_to_plane(1.0, 1.0, 'x'), 0.0)

    # Точка - "хорошая"
    def test_is_good_point01(self):
        point = R3(0.0, 3.0, 0.0)
        self.assertTrue(point.is_good_point(1.0, 2.0))

    # Точка - "плохая"
    def test_is_good_point02(self):
        point = R3(0.0, 0.0, 0.0)
        self.assertFalse(point.is_good_point(1.0, 2.0))

    # Тесты для длины вектора
    def test_length01(self):
        point = R3(0.0, 0.0, 0.0)
        self.assertEqual(point.length(), 0.0)

    def test_length02(self):
        point = R3(1.0, 0.0, 0.0)
        self.assertEqual(point.length(), 1.0)

    def test_length03(self):
        point = R3(1.0, 2.0, 2.0)
        self.assertEqual(point.length(), 3.0)
