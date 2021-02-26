import sys

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
    def __init__(self, street):
        self.street =  street
        self.is_green = False

    def __repr__(self):
        return f'{self.street.name} : {self.is_green}'

    def start_green(self):
        self.is_green = True

class Intersection:
    def __init__(self, lights):
        self.lights = lights
        self.current_green = None

    def __repr__(self):
        return f'{self.lights}'

    def next_car(self):
        if self.current_green is not None:
            stack = self.current_green.street.stack
            if stack:
                car = stack.pop(0)
                car.next_street()

    def switch_light_to(self, light):
        if self.current_green is not None:
            self.current_green.is_green = False
        self.current_green = light
        if light is not None:
            light.start_green() 


def simulation(input_filename, ):
    n_useful_intersections = 0
    with open(input_filename, 'r') as input_fp:
        D, I, S, V, F = map(int, input_fp.readline().split())
        intersections = []
        streets = {}
        lights_for_intersections = [[] for _ in range(I)]
        for _ in range(S):
            B, E, name, L = input_fp.readline().split()
            B, E, L = map(int, [B, E, L])
            street = Street(B, E, name, L)
            streets[name] = street
            lights_for_intersections[E].append(Light(street))

        cars = []
        seen_streets = set()
        for _ in range(V):
            path = input_fp.readline().split()[1:]
            street_paths = [streets[p] for p in path]
            for street in street_paths:
                seen_streets.add(street)
            cars.append(Car(street_paths))

        for intersection_id, lights in enumerate(lights_for_intersections):
            useful_lights = [light for light in lights if light.street in seen_streets]
            intersections.append(Intersection(useful_lights))
            if useful_lights:
                n_useful_intersections += 1

    light_orderings_for_intersections = [[None] * len(intersection.lights) for intersection in intersections]
    remaining_lights_for_intersections = [set(intersection.lights) for intersection in intersections]
    score = 0
    for t in range(1, D+1):
        for intersection, light_orderings, remaining_lights in zip(intersections, light_orderings_for_intersections, remaining_lights_for_intersections):
            n_lights = len(intersection.lights)
            if not n_lights:
                continue
            interval = (t - 1) % n_lights
            light_this_interval = light_orderings[interval]
            if light_this_interval is None:
                light_with_max_car_waiting = max(remaining_lights, key=lambda light: len(light.street.stack))
                if light_with_max_car_waiting.street.stack:
                    light_orderings[interval] = light_this_interval = light_with_max_car_waiting
                    remaining_lights.remove(light_this_interval)

            intersection.switch_light_to(light_this_interval)

        for intersection in intersections:
            intersection.next_car()

        for car in cars:
            if car.next_second():
                score += F + (D - t)

    # fill up None
    for intersection, light_orderings in zip(intersections, light_orderings_for_intersections):
        is_light_used = {light:False for light in intersection.lights}
        i_use = 0
        for light in light_orderings:
            is_light_used[light] = True
        for interval, light in enumerate(light_orderings):
            if light is None:
                while is_light_used[intersection.lights[i_use]]:
                    i_use += 1
                light = intersection.lights[i_use]
                light_orderings[interval] = light
                is_light_used[light] = True

    print(score)
    write(f'{input_filename}.out',n_useful_intersections,light_orderings_for_intersections,D,I,S,V,F,intersections)

def write(output_filename,n_useful_intersections,light_orderings_for_intersections,D,I,S,V,F,intersections):
    def prin(*args):
        print(*args, file=f)
    with open(output_filename, 'wt') as f:
        prin(n_useful_intersections)
        for intersection_id, orderings in enumerate(light_orderings_for_intersections):
            if not orderings:
                continue
            prin(intersection_id)
            prin(len(orderings))
            for light in orderings:
                prin(light.street.name, 1)


if __name__ == '__main__':
    input_filename = sys.argv[1]
    simulation(input_filename)
    print(f'Done {input_filename}')
