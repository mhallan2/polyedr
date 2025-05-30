from tkinter import *
from common.r3 import R3


# Размер окна
SIZE = 900
# Коэффициент гомотетии
SCALE = 1.5


def x(p):
    """преобразование x-координаты"""
    return SIZE / 2 + SCALE * p.x


def y(p):
    """ " преобразование y-координаты"""
    return SIZE / 2 - SCALE * p.y


class TkDrawer:
    """Графический интерфейс"""

    # Конструктор
    def __init__(self):
        self.root = Tk()
        self.root.title("Изображение проекции полиэдра")
        self.root.geometry(f"{SIZE + 5}x{SIZE + 5}")
        self.root.resizable(False, False)
        self.root.bind("<Control-c>", quit)
        self.canvas = Canvas(self.root, width=SIZE, height=SIZE)
        self.canvas.pack(padx=5, pady=5)

    # Завершение работы
    def close(self):
        self.root.quit()

    # Стирание существующей картинки
    def clean(self):
        self.canvas.create_rectangle(0, 0, SIZE, SIZE, fill="white")
        self.root.update()

     #Рисование линии
    def draw_line(self, p, q, line_color="black", line_width=1, dash=None):
        if dash:
            line_color = "gray"
        self.canvas.create_line(x(p), y(p), x(q), y(q), fill=line_color, width=line_width, dash=dash)
        self.root.update()

    def draw_point(self, p, c=1, point_size=2):
        # Цвета точки
        p_color = "red" if p.is_good_point(c) else "blue"

        # Рисуем точку p
        self.canvas.create_oval(
            x(p) - point_size,
            y(p) - point_size,
            x(p) + point_size,
            y(p) + point_size,
            fill=p_color,
            outline=p_color,
        )

        self.root.update()  # Обновляем холст

    def draw_axes(self, alpha, beta, gamma, c=1.0, length=100):

        def transform(p):
            return p.rz(alpha).ry(beta).rz(gamma) * c

        origin = R3(0, 0, 0)
        x_axis = transform(R3(length, 0, 0))
        y_axis = transform(R3(0, length, 0))
        z_axis = transform(R3(0, 0, length))

        self.draw_line(origin, x_axis, line_color='gray', line_width=3)
        self.draw_line(origin, y_axis, line_color='gray', line_width=3)
        self.draw_line(origin, z_axis, line_color='gray', line_width=3)

    def draw_plane_y_eq_minus_1(
        self, alpha, beta, gamma, c=1.0, size=1000, step=1, line_color='gray'
    ):

        def transform(p):
            return p.rz(alpha).ry(beta).rz(gamma) * c

        y = -1 * c
        for x in range(-size, size + 1, step):
            p1 = transform(R3(x, y, -size))
            p2 = transform(R3(x, y, size))
            self.draw_line(p1, p2, line_width=1, line_color=line_color)

        for z in range(-size, size + 1, step):
            p1 = transform(R3(-size, y, z))
            p2 = transform(R3(size, y, z))
            self.draw_line(p1, p2, line_width=1, line_color=line_color)


if __name__ == "__main__":  # pragma: no cover
    import time
    from r3 import R3

    tk = TkDrawer()
    tk.clean()
    tk.draw_line(R3(0.0, 0.0, 0.0), R3(100.0, 100.0, 0.0))
    tk.draw_line(R3(0.0, 0.0, 0.0), R3(0.0, 100.0, 0.0))
    time.sleep(5)
