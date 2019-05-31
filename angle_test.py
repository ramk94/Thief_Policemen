import numpy as np


def unit_vector(vector):
    return vector/np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.dot(v1_u.T, v2_u))/np.pi*180


a1 = np.array((0, 1)).reshape((-1, 1))
a2 = np.array((0, -1)).reshape((-1, 1))
print(angle_between(a1, a2))
