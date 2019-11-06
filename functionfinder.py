import math
import statistics
import matplotlib.pyplot as plt

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

#Calculate second differences
first_differences = [points_y[i+1]-y for i,y in enumerate(points_y[:-1])]
second_differences = [first_differences[i+1]-y for i,y in enumerate(first_differences[:-1])]
stdDev2Diff = statistics.stdev(second_differences)
if stdDev2Diff == 0:
    print("Points fit a quadratic") #ax^2+bx+c
    a = second_differences[0]/2
    new_y = [y-a*points_x[i]**2 for i,y in enumerate(points_y)]
    first_differences = [new_y[i+1]-y for i,y in enumerate(new_y[:-1])]
    b = first_differences[0]
    new_y = [y-b*points_x[i] for i,y in enumerate(new_y)]
    c = new_y[0]
    print(f"f(x)={a}x^2 + {b}x + {c}")


print(first_differences)
print(second_differences)

plt.scatter(points_x,points_y)
plt.show()