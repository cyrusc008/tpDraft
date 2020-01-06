import csv 
import math

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