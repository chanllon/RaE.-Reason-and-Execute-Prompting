Geometry_Prompt = '''
Let's use python to solve geometry question. Here are three examples how to do it,
Q: Given the images, in △ABC, it is known that ∠A=80°, ∠B=60°, DE∥BC. Then, the measure of ∠CED is ()

#reasoning:
The question involves finding the degree measure of angle ∠CED. From the exercise text and the diagram, it can be inferred that solving this problem requires the use of the triangle angle sum theorem and corresponding angles postulate.
Corresponding Angles Postulate：∠CED=180-∠C
Triangle Angle Sum Theorem:∠C=180-∠A-∠B
Information to be obtained from question texts and images: ∠A=80,∠B=60
The solution that need to be converted into Python code are: ∠A=80,∠B=60，∠C=180-∠A-∠B，∠CED=180-∠C

# solution in Python:

```
def solution():
"""The operations that need to be converted into Python code are: ∠A=80,∠B=60，∠C=180-∠A-∠B，∠CED=180-∠C"""
    angle_A = 80
    angle_B = 60
    angle_C = 180 - angle_A - angle_B
    angle_CED = 180 - angle_C
    result = angle_CED
    return  result
```


Q: "Given the images, with circle O, chord AB = 18, M is the midpoint of AB, and OM = 12, then the radius of circle O is ()"

#reasoning:
The question is to find the radius OB of the circle. It can be inferred from the exercise text and the image that solving this problem requires the Pythagorean theorem.
Pythagorean theorem: OB*OB=OM*OM+BM*BM
M is the midpoint of AB:BM=0.5*AB
Information to be obtained from question texts and images: OM=12,AB=18
The solution that need to be converted into Python code are:OM=12,AB=18,BM=0.5*AB,OB*OB=OM*OM+BM*BM

# solution in Python:
```
import math
def solution():
    """The operations that need to be converted into Python code are:OM=12,AB=18,BM=0.5*AB,OB*OB=OM*OM+BM*BM"""
    Line_AB = 18
    Line_OM = 12
    Line_BM = Line_AB / 2
    Line_OB = math.sqrt(Line_OM * Line_OM + Line_BM * Line_BM)
    result = Line_OB
    return result
```

Q: {question}
#reasoning:

# solution in Python:
```
def solution():
```
'''.strip() + '\n\n\n'