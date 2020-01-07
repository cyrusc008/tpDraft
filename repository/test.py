import numpy as np
import csv
import matplotlib.pyplot as plt
import math
import types 
from functions import read_passengers, import_speed, route_check
from statistics import mean
import argparse 

class Passenger:
    def __init__(self, start, end, speed):
        self.start = start 
        self.end = end
        self.speed = speed

    def walk_time(self): 
        times = math.sqrt((self.start[0] - self.end[0])**2 + (self.start[1] - self.end[1])**2)*self.speed
        return times 

    def __repr__(self):
        return '({}, {}, {})'.format(self.start, self.end, self.speed)

class Route:
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
            time += int(import_speed())
        return stops
    
    def plot_map(self):
        self.route = Route.read_route(route)
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

    def passenger_trip(self, passenger):
        self.route = Route.read_route(route)
        start = passenger.start
        end = passenger.end
        stops = [value for value in self.route if value[2]]
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

    def plot_bus_load(self):
        self.route = Route.read_route(route)
        self.passenger = journey.passenger
        stops = {step[2]:0 for step in self.route if step[2]}
        for passenger in self.passenger:
            trip = Journey.passenger_trip(self, passenger)
            stops[trip[0][1]] += 1
            stops[trip[1][1]] -= 1
            #check = print(trip)
        for i, stop in enumerate(stops):
            if i > 0:
                stops[stop] += stops[prev]
            prev = stop
        fig, ax = plt.subplots()
        ax.step(range(len(stops)), list(stops.values()), where='post')
        ax.set_xticks(range(len(stops)))
        ax.set_xticklabels(list(stops.keys()))
        plt.show()
        #return check

    def passenger_trip_time(self):
        bus_times = Route.timetable(route)
        self.passenger = journey.passenger
        time_bus = []
        time_walk = []
        for passenger in self.passenger:    
            walk_distance_stops = Journey.passenger_trip(self, passenger)     
            bus_checker = bus_times[walk_distance_stops[1][1]] - \
                                bus_times[walk_distance_stops[0][1]] 
            walk_checker = Passenger.walk_time(passenger)          
            if bus_checker > 0:       
                    if bus_checker >= walk_checker:
                        bus_travel = 0
                        walk_travel = walk_checker    
                    else:           
                        bus_travel = bus_checker
                        walk_travel = walk_distance_stops[0][0] * passenger.speed + \
                                      walk_distance_stops[1][0] * passenger.speed      
            else:
                bus_travel = 0
                walk_travel = walk_checker
            time_bus.append(float(bus_travel))
            time_walk.append(float(walk_travel))
        return time_bus, time_walk

    def travel_time(self, i):
        trip_values = tracker[i]
        return print(trip_values)

    def print_time_stats(self):
        bus_average = mean(Journey.passenger_trip_time(self)[0])
        walk_average = mean(Journey.passenger_trip_time(self)[1])
        print(f"Average time on bus: {bus_average:03.2f} min")
        print(f"Average walking time: {walk_average:03.2f} min")

    def __repr__(self):
        return 'Passenger List: {}'.format(self.passenger)

    def __repr__(self):
        return 'Route List: {}'.format(self.route)

route = Route('route.csv')
route.plot_map()
route_check(route)
passengers = [
    Passenger(start, end, speed)
    for start, end, speed
    in read_passengers('passengers.csv')
]
journey = Journey(route, passengers)
journey.plot_bus_load()

# route = Route("route.csv")
# route.plot_map()
# route_check(route)
# john = Passenger(start=(0,2), end=(8,1), speed=15)
# mary = Passenger(start=(0,0), end=(6,2), speed=12)
# journey = Journey(route, [mary, john])
# journey.plot_bus_load()

journey.print_time_stats()
tracker = {int(i): {'bus': journey.passenger_trip_time()[0][i], 
                    'walk': journey.passenger_trip_time()[1][i]} for i in range(len(journey.passenger))}
journey.travel_time(0)


