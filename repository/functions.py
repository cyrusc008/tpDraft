import csv 
import math

def passenger_trip(passenger, route):
    start, end, pace = passenger
    stops = [value for value in route if value[2]]
    # calculate closer stops
    ## to start
    distances = [(math.sqrt((x - start[0])**2 +
                            (y - start[1])**2), stop) for x,y,stop in stops]
    closer_start = min(distances)
    ## to end
    distances = [(math.sqrt((x - end[0])**2 +
                            (y - end[1])**2), stop) for x,y,stop in stops]
    closer_end = min(distances)
    return (closer_start, closer_end)

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