import csv 
import math
import argparse

def read_passengers(filename):
    passenger = []
    with open(filename, 'r') as data:
        reader = csv.reader(data, delimiter=',')
        headers = None
        for row in reader:
            line = [x for x in row]
            start = (int(line[0]), int(line[1]))
            end = (int(line[2]), int(line[3]))
            speed = (int(line[4]))
            data = (start, end, speed)
            passenger.append(data)
    return passenger

def import_speed():
    parser = argparse.ArgumentParser(description="Import bus speed")
    parser.add_argument("speed", help="bus speed per step", nargs='?', default=10)
    args = parser.parse_args()
    return args.speed

def route_check(route):
    """
    Checks if numbers only
    """
    cc = route.generate_cc()[1]
    cc_values = [int(x) for x in cc]
    for i in range(len(cc)):
        assert (cc_values[i] % 2) == 0