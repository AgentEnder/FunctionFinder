import math
import statistics
import matplotlib.pyplot as plt
import numpy as np

FLOAT_THRESHOLD = 0.0005

fig, axs = plt.subplots(2, 3, figsize=(9, 6))

points_x = []
points_y = []
num_points = 0
print("How many points would you like to use?")
while True:  # Get user input
    _in = input()
    try:
        num_points = int(_in)  # Try to convert to integer
        break
    except ValueError as error:
        print(f"Invalid number of points: {str(error)}")  # Not an integer

print("Enter points as `x,y`")
while len(points_x) < num_points:
    # Try to get a coordinate pair
    _in = input(f"Enter point {len(points_x)+1}: ")
    try:
        x, y = [float(i) for i in _in.split(",")]
        if x in points_x:
            raise ValueError(f"Point with x-coordinate {x} already exists")
        points_x.append(x)
        points_y.append(y)
    except ValueError as error:
        print(f"Invalid Point: {str(error)}")

# Sort coordinates
# Sort Y ordinates by values of X ordinates
points_y = [y for _, y in sorted(zip(points_x, points_y))]
points_x.sort()  # Sort X ordinates

# Calculate differences
x_differences = [points_x[i+1]-x for i, x in enumerate(points_x[:-1])]
y_differences = [points_y[i+1]-y for i, y in enumerate(points_y[:-1])]

# Originally was calculating quadratics by using 2nd differences, but that resulted in issues when x0 != 1, x1 != 2...
if len(points_x) > 2:
    # Calculate parabola that fits the first 3 points
    x1, x2, x3 = points_x[:3]
    y1, y2, y3 = points_y[:3]
    # These are derived from the matrix equations to solve for a parabola given 3 points.
    denom = (x1 - x2)*(x1 - x3)*(x2 - x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
    b = (x3**2 * (y1 - y2) + x2**2 * (y3 - y1) + x1**2 * (y2 - y3)) / denom
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1)
         * y2 + x1 * x2 * (x1 - x2) * y3) / denom

    for x, y in zip(points_x, points_y):  # Check if it fits all of the points
        if not abs(a*x**2+b*x+c - y) < FLOAT_THRESHOLD:
            axs[0, 0].set_title("Not a valid quadratic.")
            axs[0, 0].axis("off")
            break  # There is an issue.
    else:  # It fits
        print("Points fit a quadratic")  # ax^2+bx+c
        func = f"$f(x)={round(a,4)}x^2 + {round(b,4)}x + {round(c,4)}$"
        print(func)
        x_ords = list(np.arange(points_x[0]-1, points_x[-1]+2, 0.1))
        y_ords = list([a*x**2+b*x+c for x in x_ords])
        line = axs[0, 0].plot(x_ords, y_ords, label=func, linewidth=2)
        axs[0, 0].set_title(func)
        axs[0, 0].scatter(points_x, points_y)
        axs[0, 0].axhline(c='black')
else:
    axs[0, 0].set_title("Not a unique quadratic.")
    axs[0, 0].axis("off")


x_ratios = [points_x[i+1]/x for i, x in enumerate(points_x[:-1])]
y_ratios = [points_y[i+1]/y for i, y in enumerate(points_y[:-1])]

# ratio between the 2 difference arrays
deltaXYRatios = [x_differences[i]/y for i, y in enumerate(y_differences)]
# ratio between x delta and y ratio
deltaXRatioYRatios = [x_differences[i] /
                      math.log(y) for i, y in enumerate(y_ratios)]
# convert x to linear and y to linear, check ratios
ratioXRatioYRatios = [math.log(x_ratios[i])/math.log(y)
                      for i, y in enumerate(y_ratios)]
# convert x to linear, check ratios.
ratioXDeltaYRatios = [
    math.log(x_ratios[i])/y for i, y in enumerate(y_differences)]


# The closer to 0 xError is, the more likely f(x) is a x-typed function.
linearError = 0 if len(deltaXYRatios) < 2 else statistics.stdev(deltaXYRatios)
exponentialError = 0 if len(
    deltaXRatioYRatios) < 2 else statistics.stdev(deltaXRatioYRatios)
powerError = 0 if len(ratioXRatioYRatios) < 2 else statistics.stdev(
    ratioXRatioYRatios)
logError = 0 if len(ratioXDeltaYRatios) < 2 else statistics.stdev(
    ratioXDeltaYRatios)

math.log

#print(stdDevXDiff, stdDevXRatio, stdDevYDiff, stdDevYRatio)

if linearError == 0:  # Add a constant to X and Y
    dx = x_differences[0]
    dy = y_differences[0]
    m = dy/dx
    c = points_y[0]-points_x[0]*m
    print("Points fit a linear function.")
    func = f"$f(x)={round(m,4)}x+{round(c,4)}$"
    x_ords = list(np.arange(points_x[0]-1, points_x[-1]+2, 0.1))
    y_ords = list([m*x+c for x in x_ords])
    line = axs[0, 1].plot(x_ords, y_ords, label=func, linewidth=2)
    axs[0, 1].set_title(func)
    axs[0, 1].scatter(points_x, points_y)
    axs[0, 1].axhline(c='black')
    print(func)
else:
    axs[0, 1].set_title("Not a valid linear function")
    axs[0, 1].axis("off")

if abs(exponentialError) < FLOAT_THRESHOLD:  # Multiply by a constant on Y
    print("Points fit on an exponential")
    dx = x_differences[0]
    ry = y_ratios[0]
    #ry = b^dx
    b = ry**(1/dx)
    a = points_y[0]/(b**points_x[0])
    func = f"$f(x)={round(a,4)}*{round(b,4)}^x$"
    x_ords = list(np.arange(points_x[0]-1, points_x[-1]+2, 0.1))
    y_ords = list([a*b**x for x in x_ords])
    line = axs[1, 0].plot(x_ords, y_ords, label=func, linewidth=2)
    axs[1, 0].set_title(func)
    axs[1, 0].scatter(points_x, points_y)
    axs[1, 0].axhline(c='black')
    print(func)
else:
    axs[1, 0].set_title("Not a valid exponential function")
    axs[1, 0].axis("off")

if abs(powerError) < FLOAT_THRESHOLD:
    print("Points fit on a power curve")
    rx = x_ratios[0]
    ry = y_ratios[0]
    k = math.log(ry, rx)
    a = points_y[1]/points_x[1]**k
    func = f"$f(x)={round(a,4)}*x^{{{round(k,4)}}}$"
    x_ords = list(np.arange(points_x[0]-1, points_x[-1]+2, 0.1))
    y_ords = list([a*x**k for x in x_ords])
    line = axs[1, 1].plot(x_ords, y_ords, label=func, linewidth=2)
    axs[1, 1].set_title(func)
    axs[1, 1].scatter(points_x, points_y)
    axs[1, 1].axhline(c='black')
    print(func)
else:
    axs[1, 1].set_title("Not a valid power function.")
    axs[1, 1].axis("off")

if abs(logError) < FLOAT_THRESHOLD:
    print("Points fit on a logarithmic curve")
    rx = x_ratios[0]
    dy = y_ratios[0]
    # f(x2) = f(x1) + bln(c)
    # f(x) = a+bln(x)
    # a = f(x)-bln(x)
    b = (points_y[1]-points_y[0])/math.log(rx)
    a = points_y[0]-b*math.log(points_x[0])
    func = f"f(x)={round(a,4)}+{round(b,4)}*ln(x)"
    x_ords = list(np.arange(points_x[0]-1, points_x[-1]+2, 0.1))
    if x_ords[0] <= 0:
        # math.log throws an error if x < 0.
        x_ords = [x for x in x_ords if x > 0]
    y_ords = list([a+b*math.log(x) for x in x_ords])
    line = axs[1, 2].plot(x_ords, y_ords, label=func, linewidth=2)
    axs[1, 2].set_title(func)
    axs[1, 2].scatter(points_x, points_y)
    axs[1, 2].axhline(c='black')
    print(func)
else:
    axs[1, 2].set_title("Not a valid logarithmic function.")
    axs[1, 2].axis("off")

tableData = list(zip(points_x, points_y))
#tableData.append([[points_x[i],y] for i,y in enumerate(points_y)])
tbl = axs[0, 2].table(tableData, colLabels=['x', 'y'], loc="center")
tbl.auto_set_font_size(True)
axs[0, 2].axis("off")

# for ax in axs.reshape(-1):


plt.subplots_adjust(left=0.05, right=0.95, top=0.95,
                    bottom=0.05, hspace=.5, wspace=0.4)
plt.title = "Functions fit for given points:"
plt.show()
