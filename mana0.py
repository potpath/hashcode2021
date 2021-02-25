from collections import defaultdict

def sol(D,I,S,V,F,streets,cars,from_ins,to_ins):
    in_street_count = [defaultdict(int) for _ in range(I)]
    street_ws = [0] * S
    for car in cars:
        for istreet in car:
            street_ws[istreet] += 1

    schs = []
    for inters in to_ins:
        sch = []
        for ist in inters:
            w = street_ws[ist]
            if w == 0:
                continue
            sch.append((ist, w))
        schs.append(sch)

    return schs


street_name_map = {}

def read():
    D,I,S,V,F = map(int, input().split())
    streets = []
    cars = []
    from_ins = [[] for _ in range(I)]
    to_ins = [[] for _ in range(I)]
    for _ in range(S):
        B,E,name,L = input().split()
        sid = len(street_name_map)
        street_name_map[name] = sid
        B = int(B)
        E = int(E)
        L = int(L)
        streets.append((B,E,name,L))
        from_ins[B].append(sid)
        to_ins[E].append(sid)

    for _ in range(V):
        _, *names = input().split()
        car = list(map(street_name_map.__getitem__, names))
        cars.append(car)

    return D,I,S,V,F,streets,cars,from_ins,to_ins


def write(schs,D,I,S,V,F,streets,cars,from_ins,to_ins):
    print(I)
    for iin, sch in enumerate(schs):
        print(iin)
        if not sch:
            print(1)
            print(streets[to_ins[iin][0]][2], 1)
            continue
        print(len(sch))
        for sid, duration in sch:
            print(streets[sid][2], duration)


if __name__ == '__main__':
    inps = read()
    write(sol(*inps), *inps)
