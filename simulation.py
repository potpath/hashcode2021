from collections import defaultdict


class Street:
    def __init__(self, B, E, name, L):
        self.B = B
        self.E = E
        self.name = name
        self.L = L


class Car:
    def __init__(self, path):
        self.path = path


class Light:
    def __init__(self, name, T):
        self.name =  name
        self.T = T


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
            cars.append(Car(path))

    with open(output_filename, 'r') as output_fp:
        A = int(output_fp.readline())
        intersections = defaultdict(list)
        for _ in range(A):
            i = int(output_fp.readline())
            E = int(output_fp.readline())
            for _ in range(E):
                name, T = output_fp.readline().split()
                T = int(T)
                intersections[i].append(Light(name, T))

    for t in range(D):
        pass






if __name__ == '__main__':
    simulation('a.txt', 'out_a_example.txt')