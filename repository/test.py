import numpy as np
import csv
import matplotlib.pyplot as plt
import math

class Passenger():
    def __init__(self, start, end, speed):
        self.start = start 
        self.end = end
        self.speed = speed

    def walk_time(self): 
        times = math.sqrt((self.start[0] - self.end[0])**2 + (self.start[1] - self.end[1])**2)*self.speed
        return times 

class Route():

    route = []

    def __init__(self, filename):
        self.filename = filename 

    def timetable(self):
        self.route = []
        with open(self.filename, 'r') as data:
            reader = list(csv.reader(data, delimiter=','))
            headers = None
            for row in reader:
                line = [x for x in row]
                position = (int(line[0]), int(line[1]), line[2])
                self.route.append(position)
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

class Journey(Passenger, Route):
    pass

route = Route('route.csv')
john = Passenger(start=(0,2), end=(8,1), speed=15)
print(john.walk_time())
print(route.timetable())
route.plot_map()
start_point, cc = route.generate_cc()
print((f"The bus route starts at {start_point} and\n"
       f"it's described by this chain code:\n{cc}"))