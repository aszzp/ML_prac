import numpy as np
a = np.array([[1,2,3,4],[1,2,3,4]])
a **= 2
b = a.std(axis=0)
print(b)