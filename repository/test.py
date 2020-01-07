import numpy as np
import csv
import matplotlib.pyplot as plt
import math
import types 
from functions import read_passengers

class Passenger:
    def __init__(self, start, end, speed):
        self.start = start 
        self.end = end
        self.speed = speed

    def walk_time(self): 
        times = math.sqrt((self.start[0] - self.end[0])**2 + (self.start[1] - self.end[1])**2)*self.speed
        return print(f" Walking Time: {times} minutes") 

    def __repr__(self):
        return '({}, {}, {})'.format(self.start, self.end, self.speed)

class Route:

    route = []

    def __init__(self, filename):
        self.filename = filename 
    
    def read_route(self):
        self.route = []
        with open(self.filename, 'r') as data:
            reader = list(csv.reader(data, delimiter=','))
            headers = None
            for row in reader:
                line = [x for x in row]
                position = (int(line[0]), int(line[1]), line[2])
                self.route.append(position)    
        return self.route    

    def timetable(self):
        self.route = Route.read_route(self)
        time = 0
        stops = {}
        for step in self.route:
            if step[2]:
                stops[step[2]] = time
            time += 10
        return stops 
    
    def plot_map(self):
        max_x = max([n[0] for n in self.route]) + 5 # adds padding
        max_y = max([n[1] for n in self.route]) + 5
        grid = np.zeros((max_y, max_x))
        for x,y,stop in self.route:
            grid[y, x] = 1
            if stop:
                grid[y, x] += 1
        fig, ax = plt.subplots(1, 1)
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect('equal', 'datalim')
        plt.show()
    
    def generate_cc(self):
        start = self.route[0][:2]
        cc = []
        freeman_cc2coord = {0: (1, 0),
                            1: (1, -1),
                            2: (0, -1),
                            3: (-1, -1),
                            4: (-1, 0),
                            5: (-1, 1),
                            6: (0, 1),
                            7: (1, 1)}
        freeman_coord2cc = {val: key for key,val in freeman_cc2coord.items()}
        for b, a in zip(self.route[1:], self.route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(str(freeman_coord2cc[(x_step, y_step)]))
        return start, ''.join(cc)
    
    def __repr__(self):
        return '{}'.format(self.route)

class Journey:
    def __init__(self, route, passenger):
        self.route = route
        self.passenger = passenger

    def passenger_trip(self):
        start_one = [i[0] for i in [x.start for x in self.passenger]]
        start_two = [i[1] for i in [x.start for x in self.passenger]]
        end_one = [i[0] for i in [x.end for x in self.passenger]]
        end_two = [i[1] for i in [x.end for x in self.passenger]]
        self.route = Route.read_route(route)
        stops = [value for value in self.route if value[2]]
        # calculate closer stops
        ## to start
        for i in range(len(start_one)):
            distances = [(math.sqrt((x - start_one[i])**2 +
                                    (y - start_two[i])**2), stop) for x,y,stop in stops]
            closer_start = min(distances)
            ## to end
            distances = [(math.sqrt((x - end_one[i])**2 +
                                    (y - end_two[i])**2), stop) for x,y,stop in stops]
            closer_end = min(distances)

        return (closer_start, closer_end)

    def plot_bus_load(self):
        self.route = Route.read_route(route)
        self.passenger = passengers 
        stops = {step[2]:0 for step in self.route if step[2]}
        for passenger in self.passenger:
            trip = Journey.passenger_trip(self)
            stops[trip[0][1]] += 1
            stops[trip[1][1]] -= 1
        for i, stop in enumerate(stops):
            if i > 0:
                stops[stop] += stops[prev]
            prev = stop
        fig, ax = plt.subplots()
        ax.step(range(len(stops)), list(stops.values()), where='post')
        ax.set_xticks(range(len(stops)))
        ax.set_xticklabels(list(stops.keys()))
        plt.show()

    def __repr__(self):
        return 'Passenger List: {}'.format(self.passenger)

    def __repr__(self):
        return 'Route List: {}'.format(self.route)

route = Route('route.csv')
john = Passenger(start=(0,2), end=(8,1), speed=15)
john.walk_time()
print(route.timetable())
route.plot_map()
start_point, cc = route.generate_cc()
print((f"The bus route starts at {start_point} and\n"
       f"it's described by this chain code:\n{cc}"))
passengers = [
    Passenger(start, end, speed)
    for start, end, speed
    in read_passengers('passengers.csv')
]
journey = Journey(route, passengers)
#print(passengers.__repr__())
#print(route)
#print(journey.passenger)
#print(journey.route)
#print(passengers.start)
journey.plot_bus_load()

test_list = [((0, 2), (8, 1), 15)]
test = [Passenger(start, end, speed) for start, end, speed in test_list]
start = [x.start for x in passengers]
end = [x.end for x in passengers]
speed = [x.speed for x in passengers]
#print(start)
#print(end)
#print(speed)