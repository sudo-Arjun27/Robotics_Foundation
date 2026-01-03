import math as mt

#delcaring vectors as (x,y)

v1=(2,3)
v2=(5,6)

#peforming vector addition
sum=(v1[0]+v2[0], v1[1]+v2[1])
print(f"The addition of vectors is {sum}")


#scaling
scale=3
scaled1=(scale*v1[0], scale*v1[1])
scaled2=(scale*v2[0], scale*v2[1])

print(f"The scaled output of the vectors 1 and 2 are {scaled1} and {scaled2} respectively")

# Magnitude ot the length

mag = mt.sqrt(v1[0]**2 + v1[1]**2)
mag1 = mt.sqrt(v1[0]**2 + v1[1]**2)
print(f"Magnitude of 1 is {mag} and the Magnitude of 2 is {mag1}")