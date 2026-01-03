import math as mt
def apply_transform(matrix, vector):
    x = matrix[0][0]*vector[0] + matrix[0][1]*vector[1]
    y = matrix[1][0]*vector[0] + matrix[1][1]*vector[1]
    return (x, y)

scale_matrix = (
    (2, 0),
    (0, 1)
)

point = (1, 1)

scaled_point = apply_transform(scale_matrix, point)
print("Scaled point:", scaled_point)

theta = mt.radians(90)

rotation_matrix = (
    (mt.cos(theta), -mt.sin(theta)),
    (mt.sin(theta),  mt.cos(theta))
)

point = (1, 0)
rotated_point = apply_transform(rotation_matrix, point)

print("Rotated point:", rotated_point)
    