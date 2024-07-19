Geometry_Prompt = '''
Q: Given the images, in △ABC, it is known that ∠A=80°, ∠B=60°, DE∥BC. Then, the measure of ∠CED is ()

# solution in Python:

def solution():
"""Given the images, in △ABC, it is known that ∠A=80°, ∠B=60°, DE∥BC. Then, the measure of ∠CED is ()"""
    angle_A = 80
    angle_B = 60
    angle_C = 180 - angle_A - angle_B
    angle_CED = 180 - angle_C
    result = angle_CED
    return  result




Q: In the images, where AB is parallel to CD, the line EF intersects AB at point E and intersects CD at point F. Line EG bisects angle BEF, intersecting CD at point G. Given that angle 1 is 50°, the measure of angle 2 is ()


# solution in Python:

def solution():
    """In the images, where AB is parallel to CD, the line EF intersects AB at point E and intersects CD at point F. Line EG bisects angle BEF, intersecting CD at point G. Given that angle 1 is 50°, the measure of angle 2 is ()"""
    angle_1 = 50
    angle_BEF  = 180 - angle_1
    angle_BEG = angle_BEF / 2
    angle_2 = angle_BEG
    result = angle_2
    return result



Q: {question}


# solution in Python:


'''.strip() + '\n\n\n'