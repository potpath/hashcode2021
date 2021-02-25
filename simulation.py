from typing import Dict

class Street:
    def __init__(self, B, E, name, L):
        self.B = B
        self.E = E
        self.name = name
        self.L = L
        self.stack = []

    def __repr__(self):
        return f'{self.name} : {self.stack}'


class Car:
    def __init__(self, path: list):
        self.path = path
        self.i_street = 0
        self.until_end = 0
        self.current_street.stack.append(self)

    def __repr__(self):
        return f'{self.current_street} : {self.until_end}'

    @property
    def current_street(self) -> Street:
        return self.path[self.i_street]

    # return is_finish
    def next_second(self):
        if self.until_end > 0:
            self.until_end -= 1
            if self.until_end == 0:
                if self.i_street == len(self.path) - 1:
                    return True
                self.current_street.stack.append(self)
            return False

    def next_street(self):
        self.i_street += 1
        self.until_end = self.current_street.L


class Light:
    def __init__(self, street, T):
        self.street =  street
        self.T = T
        self.is_green = False
        self.until_red = T

    def __repr__(self):
        return f'{self.street.name} : {self.is_green} : {self.until_red}'

    def start_green(self):
        self.is_green = True
        self.until_red = self.T

class Intersection:
    def __init__(self, lights):
        self.lights = lights
        self.i_current_green = 0
        self.current_green.start_green()

    def __repr__(self):
        return f'{self.lights}'

    @property
    def current_green(self) -> Light:
        return self.lights[self.i_current_green]

    def next_car(self):
        if self.current_green.street.stack:
            car = self.current_green.street.stack.pop(0)
            car.next_street()

    def next_second(self):
        if self.current_green.until_red:
            self.current_green.is_green = False
            self.i_current_green = (self.i_current_green + 1) % len(self.lights)
            self.current_green.start_green()

        self.current_green.until_red -= 1


def simulation(input_filename, output_filename):
    with open(input_filename, 'r') as input_fp:
        D, I, S, V, F = map(int, input_fp.readline().split())
        streets = {}
        for _ in range(S):
            B, E, name, L = input_fp.readline().split()
            B, E, L = map(int, [B, E, L])
            streets[name] = Street(B, E, name, L)
        cars = []
        for _ in range(V):
            path = input_fp.readline().split()[1:]
            cars.append(Car([streets[p] for p in path]))

    with open(output_filename, 'r') as output_fp:
        A = int(output_fp.readline())
        intersections = {}
        for _ in range(A):
            i = int(output_fp.readline())
            E = int(output_fp.readline())
            lights = []
            for _ in range(E):
                name, T = output_fp.readline().split()
                T = int(T)
                lights.append(Light(streets[name], T))
            intersections[i] = Intersection(lights)

    score = 0
    for t in range(1, D):
        for intersection in intersections.values():
            intersection.next_car()
        for car in cars:
            if car.next_second():
                score += F + (D - t)
        for intersection in intersections.values():
            intersection.next_second()
    print(score)


if __name__ == '__main__':
    simulation('b.txt', 'b.txt.out')