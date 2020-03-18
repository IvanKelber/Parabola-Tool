import math

def find_pivot_column(row):
    for i in range(0, len(row)):
        if row[i] != 0:
            return i
    return 0


def reduce_matrix(matrix):
    for i in range(len(matrix) - 1):
        #switch rows if necessary
        pc = find_pivot_column(matrix[i]) #initializes pivot column to first row
        next_row = i
        for j in range(len(matrix) - i): #finds row with lower pivot column
            if find_pivot_column(matrix[i + j]) < pc:
                pc = find_pivot_column(matrix[i + j])
                next_row = i + j
        if next_row != i:
            matrix[i], matrix[next_row] = matrix[next_row], matrix[i]
        #executes row operations on successive rows
        for j in range(1, len(matrix) - i):
            if matrix[i][pc] != 0.0:
                multiplier = matrix[i + j][pc] * -1 / matrix[i][pc]
            else:
                multiplier = 0
            for k in range(0, len(matrix[i])):
                matrix[i + j][k] += matrix[i][k] * multiplier
    return matrix

#takes x and y values of three points and returns list of coefficients a, b and c of standard parabola equation
#takes as input a list of the form[[x1,y1],[x2,y2],[x3,y3]]
def find_parabola_coefficients(points):
    x1,x2,x3,y1,y2,y3 = points[0][0],points[1][0],points[2][0],points[0][1],points[1][1],points[2][1]
    x1,x2,x3,y1,y2,y3 = float(x1),float(x2),float(x3),float(y1),float(y2),float(y3)
    #checks to see that points form a valid parabola:
    if x1 == x2  or x2 == x3 or x1 == x3 or (y2 - y1) / (x2 - x1) == (y3 - y1) / (x3 - x1):
        return [0, 0, 0] #returning [0, 0, 0] will be treated as an error message
    #solves for a, b and c
    lin_eqs = [[x1**2, x1, 1, y1],[x2**2, x2, 1, y2],[x3**2, x3, 1, y3]]
    lin_eqs = reduce_matrix(lin_eqs)
    c = lin_eqs[2][3] / lin_eqs[2][2]
    b = ((lin_eqs[1][3] - (c * lin_eqs[1][2]))) / lin_eqs[1][1]
    a = ((lin_eqs[0][3] - (c * lin_eqs[0][2]) - (b * lin_eqs[0][1]))) / lin_eqs[0][0]
    return [a, b, c]


def find_standard_parabola(points): #takes as input a list of the form[[x1,y1],[x2,y2],[x3,y3]]
    coefficients = find_parabola_coefficients(points)
    a, b, c = coefficients[0], coefficients[1], coefficients[2]
    #returns equation
    if a == 0:
        return "points do not form a valid parabola"
    return [a, 0, 0, b, -1, c]

#print find_standard_parabola([[-1,7],[0,3],[1,18]])

#rotates a point, represented as a list of two values, by an angle, counter-clockwise around the origin
#input angle is in radians
def rotate_point(point, angle):
    a, b = math.sin(angle), math.cos(angle)
    new_point = [point[0] * b - point[1] * a, point[0] * a + point[1] * b]
    #cleans up rounding errors
    for i in range(0, len(new_point)):
        new_point[i] = (int(round(new_point[i] * 1000000)) + 0.0) / 1000000
    return new_point

#takes a point and angle and returns list of coefficients b and c in the linear equation x + by + c = 0
#for a line going through the given point at the given angle. Input angle is in radians
def get_linear_equation(point, angle):
    slope = math.tan(angle)
    slope = (int(round(slope * 1000000)) + 0.0) / 1000000 #cleans up rounding errors
    return [-1 / slope, (point[1] / slope) - point[0]]

#rotates a parabola counter-clockwise around origin, given a list of the coefficients of a standard parabola,
#a, b and c and the angle of rotation
#input angle is in radians.
def rotate_parabola(coefficients, angle):
    a, b, c, angle = float(coefficients[0]), float(coefficients[1]), float(coefficients[2]), angle % math.pi
    old_focus = [(b * -1) / (2 * a), c - ((b**2 - 1) / (4 * a))]
    old_directrix_y_value = c - ((b**2 + 1) / (4 * a))
    if angle != 0:
        focus = rotate_point(old_focus, angle)
        directrix_point = rotate_point([0, old_directrix_y_value], angle)
        #returns list of coefficients a and b in the linear equation x + by + c = 0 for the new directrix
        directrix_coefficients = get_linear_equation(directrix_point, angle)
        print(focus)
        print(old_directrix_y_value)
        #uses general formula for a parabola to find coefficients for equation
        B, C, F1, F2 = directrix_coefficients[0], directrix_coefficients[1], focus[0], focus[1]
        a = round((1 / (B**2 + 1)) - 1, 2)
        b = round(2 * B / (B**2 + 1), 2)
        c = round((B**2 / (B**2 + 1)) - 1, 2)
        d = round(2 * C / (B**2 + 1) + 2 * F1, 2)
        e = round(2 * B * C / (B**2 + 1) + 2 * F2, 2)
        f = round(C**2 / (B**2 + 1) - F1**2 - F2**2, 2)
        return [a, b, c, d, e, f]
    else:
        return [round(a, 2), 0, 0, round(b, 2), -1, round(c, 2)]

#takes as input a set of three points in the same list format as find_standard_parabola, along with
#an angle and returns an equation for a parabola passing through those points whose axis of symmetry
#is rotated by the given angle
def find_general_parabola(points, angle):
    angle = angle % math.pi
    if angle == 0:
        return find_standard_parabola(points)
    else:
        for i in range(len(points)):
            points[i] = rotate_point(points[i], -angle)
        coefficients_to_rotate = find_parabola_coefficients(points)
        if coefficients_to_rotate[0] == 0:
            return "points do not form a valid parabola at this angle"
        else:
            return rotate_parabola(coefficients_to_rotate, angle)