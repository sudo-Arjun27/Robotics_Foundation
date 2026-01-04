import math

def apply_transform(matrix, vector):
    x = matrix[0][0]*vector[0] + matrix[0][1]*vector[1]
    y = matrix[1][0]*vector[0] + matrix[1][1]*vector[1]
    return (x, y)

theta = math.radians(45)

rotation = (
    (math.cos(theta), -math.sin(theta)),
    (math.sin(theta),  math.cos(theta))
)

point = (2, 1)
rotated = apply_transform(rotation, point)

print("Rotated point:", rotated)

def inverse_rotation(matrix):
    return (
        (matrix[0][0], matrix[1][0]),
        (matrix[0][1], matrix[1][1])
    )

rotation_inv = inverse_rotation(rotation)

recovered = apply_transform(rotation_inv, rotated)
print("Recovered point:", recovered)
