from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def angle(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    def angle(self):
        return self.p.angle_vector(self.q)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        self.p1 = None
        self.p2 = None
        self.flag = True
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self.max_angle = 0
        if a.dist(b) >= a.dist(c) and a.dist(b) >= b.dist(c):
            self.p1 = a
            self.p2 = b
        elif a.dist(c) >= a.dist(b) and a.dist(c) >= b.dist(c):
            self.p1 = a
            self.p2 = c
        else:
            self.p1 = c
            self.p2 = b
        self.max_angle = self.p1.angle_vector(self.p2)

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def angle(self):
        return self.max_angle

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            if self.points.first().dist(self.points.last()) == \
                    self.p1.dist(self.p2):
                self.flag = False

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                if p.dist(self.points.first()) == \
                        self.p1.dist(self.p2):
                    self.flag = False
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                if p.dist(self.points.last()) == \
                        self.p1.dist(self.p2):
                    self.flag = False
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)
            if not self.flag:
                self.p1 = self.points.first()
                self.p2 = self.points.last()
                self.max_angle = self.p1.angle_vector(self.p2)
                for n in range(self.points.size()):
                    if self.points.first().dist(self.points.last()) > \
                            self.p1.dist(self.p2):
                        self.p1 = self.points.first()
                        self.p2 = self.points.last()
                        self.max_angle = self.p1.angle_vector(self.p2)
                        self.flag = True
                    elif self.points.first().dist(self.points.last()) == \
                            self.p1.dist(self.p2) \
                            and self.points.first(). \
                            angle_vector(self.points.last()) > \
                            self.max_angle:
                        self.max_angle = self.points.first(). \
                            angle_vector(self.points.last())
                        self.p1 = self.points.first()
                        self.p2 = self.points.last()
                        self.flag = True
                    self.points.push_last(self.points.pop_first())
            else:
                if t.dist(self.points.first()) > \
                        self.p1.dist(self.p2):
                    self.p1 = t
                    self.p2 = self.points.first()
                    self.flag = True
                    self.max_angle = self.p1.angle_vector(self.p2)
                elif t.dist(self.points.last()) > \
                        self.p1.dist(self.p2):
                    self.p1 = t
                    self.p2 = self.points.last()
                    self.flag = True
                    self.max_angle = self.p1.angle_vector(self.p2)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
