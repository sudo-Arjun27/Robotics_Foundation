#vectors 
basis_x = (5, 7)   
basis_y = (3, 0)   

# Coefficients
a = -1
b = 8

# Linear combination
move_x = a * basis_x[0] + b * basis_y[0]
move_y = a * basis_x[1] + b * basis_y[1]

movement = (move_x, move_y)

print("movement vector:", movement)
