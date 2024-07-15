import numpy as np

def generate_sphere_points(radius, num_points):
    points = []
    
    for _ in range(num_points):
        theta = np.arccos(2 * np.random.rand() - 1)  # theta: [0, pi]
        phi = 2 * np.pi * np.random.rand()           # phi: [0, 2pi]

        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)

        points.append((x, y, z))
    
    return points


def check_point_in_sphere(point, radius):
    x, y, z = point
    distance_squared = x**2 + y**2 + z**2
    radius_squared = radius**2

    if distance_squared <= radius_squared:
        return True
    else:
        return False
