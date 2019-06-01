import numpy as np

# build orientation unit vectors
current_direction = np.array([-1, 1]).reshape((-1, 1))
current_direction_unit = current_direction / np.linalg.norm(current_direction)
base_direction = np.array([0, 1]).reshape((-1, 1))
base_direction_unit = base_direction / np.linalg.norm(base_direction)

# build center vectors
current_center = np.array([0, 0]).reshape((-1, 1))
target = np.array([1, -1]).reshape((-1, 1))

# calculate the angle between centers
delta = target - current_center
dot = np.dot(base_direction_unit.T, delta)
det = np.cross(delta.flatten(), base_direction_unit.flatten())
theta = np.arctan2(det, dot) * 180 / np.pi

# calculate the angle between orientations
dot = np.dot(base_direction_unit.T, current_direction_unit)
det = np.cross(current_direction_unit.flatten(), base_direction_unit.flatten())
alpha = np.arctan2(det, dot) * 180 / np.pi

print(theta, alpha)

gamma = theta - alpha
print(gamma)
