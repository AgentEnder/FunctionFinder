import math
import statistics
import matplotlib.pyplot as plt
import numpy as np

points_x = []
points_y = []
num_points = 0
print("How many points would you like to use?") 
while True: #Get user input
    _in = input()
    try:
        num_points = int(_in) #Try to convert to integer
        break
    except ValueError as error:
        print(f"Invalid number of points: {str(error)}") #Not an integer

print("Enter points as `x,y`")
while len(points_x) < num_points:
    _in = input(f"Enter point {len(points_x)+1}: ") #Try to get a coordinate pair
    try:
        x, y = [float(i) for i in _in.split(",")]
        if x in points_x:
            raise ValueError(f"Point with x-coordinate {x} already exists")
        points_x.append(x)
        points_y.append(y)
    except ValueError as error:
        print(f"Invalid Point: {str(error)}")

# Sort coordinates
points_y = [y for _,y in sorted(zip(points_x, points_y))] # Sort Y ordinates by values of X ordinates
points_x.sort() # Sort X ordinates

#Calculate differences
x_differences = [points_x[i+1]-x for i,x in enumerate(points_x[:-1])]
y_differences = [points_y[i+1]-y for i,y in enumerate(points_y[:-1])]

if len(points_x) > 2: #Originally was calculating quadratics by using 2nd differences, but that resulted in issues when x0 != 1, x1 != 2...
    x1, x2, x3 = points_x[:3]
    y1, y2, y3 = points_y[:3]
    denom = (x1 - x2)*(x1 - x3)*(x2 - x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
    b = (x3**2 * (y1 - y2) + x2**2 * (y3 - y1) + x1**2 * (y2 - y3)) / denom
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom
    
    for x, y in zip(points_x, points_y):
        if not a*x**2+b*x+c == y:
            break
    else:
        print("Points fit a quadratic") #ax^2+bx+c
        func = f"f(x)={a}x^2 + {b}x + {c}"
        print(func)
        x_ords = list(np.arange(points_x[0]-1,points_x[-1]+2, 0.1))
        y_ords = list([a*x**2+b*x+c for x in x_ords])
        line = plt.plot(x_ords,y_ords, label=func, linewidth=4)
    


x_ratios = [points_x[i+1]/x for i,x in enumerate(points_x[:-1])]
y_ratios = [points_y[i+1]/y for i,y in enumerate(points_y[:-1])]

stdDevXDiff = statistics.stdev(x_differences)
stdDevYDiff = statistics.stdev(y_differences)
stdDevXRatio = statistics.stdev(x_ratios)
stdDevYRatio = statistics.stdev(y_ratios)

#print(stdDevXDiff, stdDevXRatio, stdDevYDiff, stdDevYRatio)

if stdDevXDiff == 0: #Add a constant to X
    if stdDevYDiff == 0: #Add a constant to Y
        dx = x_differences[0]
        dy = y_differences[0]
        m = dy/dx
        c = points_y[0]-points_x[0]*m
        print("Points fit a linear function.")
        func = f"f(x)={m}x+{c}"
        x_ords = list(np.arange(points_x[0]-1,points_x[-1]+2, 0.1))
        y_ords = list([m*x+c for x in x_ords])
        line = plt.plot(x_ords,y_ords, label=func, linewidth=2)
        print(func)
    if stdDevYRatio == 0: #Multiply by a constant on Y
        print("Points fit on an exponential")
        dx = x_differences[0]
        ry = y_ratios[0]
        #ry = b^dx
        b = ry**(1/dx)
        a = points_y[0]/(b**points_x[0])
        func = f"f(x)={a}*{b}^x"
        x_ords = list(np.arange(points_x[0]-1,points_x[-1]+2, 0.1))
        y_ords = list([a*b**x for x in x_ords])
        line = plt.plot(x_ords,y_ords, label=func, linewidth=2)
        print(func)

    pass

plt.scatter(points_x,points_y)
plt.legend()
plt.show()