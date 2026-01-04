import math

def apply_transform(matrix, vector):
    x = matrix[0][0]*vector[0] + matrix[0][1]*vector[1]
    y = matrix[1][0]*vector[0] + matrix[1][1]*vector[1]
    return (x, y)

def multiply_matrices(A, B):
    return (
        (
            A[0][0]*B[0][0] + A[0][1]*B[1][0],
            A[0][0]*B[0][1] + A[0][1]*B[1][1]
        ),
        (
            A[1][0]*B[0][0] + A[1][1]*B[1][0],
            A[1][0]*B[0][1] + A[1][1]*B[1][1]
        )
    )

theta = math.radians(90)

rotation = (
    (math.cos(theta), -math.sin(theta)),
    (math.sin(theta),  math.cos(theta))
)

scale = (
    (2, 0),
    (0, 1)
)

point = (1, 1)

combined_1 = multiply_matrices(scale, rotation)
combined_2 = multiply_matrices(rotation, scale)

print("Scale then Rotate:", apply_transform(combined_1, point))
print("Rotate then Scale:", apply_transform(combined_2, point))