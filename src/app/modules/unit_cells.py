import modules.stl_generator_pymesh as stl_gen
import pymesh
import numpy as np
import math

def get_cubic_unit_cell_ratios(support_length, cube_side_lenght, support_side_length):
    support_structure_volume = (3*(support_side_length*(support_length**2)))-(2*(support_length**3))
    cube_volume = (cube_side_lenght**3)
    unit_cell_max_volume = support_side_length**3

    print(f"Max Space volume: {unit_cell_max_volume} | Cube volume: {cube_volume} | Support only volume: {support_structure_volume} (ratio : {support_structure_volume/unit_cell_max_volume})")





import math

def calculate_support_side_length(f2_ratio, support_length):
    # Ensure f2_ratio and support_length are positive
    if f2_ratio <= 0 or support_length <= 0:
        raise ValueError("f2_ratio and support_length must be positive and greater than 0.")
    
    # Check if f2_ratio < 1
    if f2_ratio < 1:
        # Calculate the inner term to ensure it's non-negative
        inner_sqrt_term = (support_length**6 * (f2_ratio - 1)) / f2_ratio**3
        if inner_sqrt_term < 0:
            raise ValueError("The term under the square root is negative, leading to a math domain error.")

    # Calculating intermediate components
    term1 = f2_ratio * math.sqrt(max(0, (support_length**6 * (f2_ratio - 1)) / f2_ratio**3)) + support_length**3
    inner_term = term1 / f2_ratio

    # Calculate support_side_length based on the derived equation
    support_side_length = -((f2_ratio * (inner_term ** (2 / 3)) + support_length**2) /
                            (f2_ratio * (inner_term ** (1 / 3))))

    return support_side_length






def calculate_mesh_volume(mesh):
    unique_faces = set()
    volume = 0.0

    for face in mesh.faces:
        # Sort the vertices within the face to check for duplicates
        sorted_face = tuple(sorted(face))

        # Skip this face if it's already in the set (i.e., it's a duplicate)
        if sorted_face in unique_faces:
            continue

        # Add the face to the set as we've now processed it
        unique_faces.add(sorted_face)

        # Calculate the signed volume of the tetrahedron formed by this face and the origin
        v0, v1, v2 = mesh.vertices[face]
        tetra_volume = np.dot(v0, np.cross(v1, v2)) / 6.0
        volume += tetra_volume

    return abs(volume)  # Return the absolute value to get the total volume


def generate_cubic_unit_cell(cubic_center: list = [0, 0, 0], support_length: int = 0, cube_side_lenght: float = 0.0, support_side_length: float = 0.0):
    # Unit cell based of the "A Highly Efficient Energy Harvesting Circuit Using Luneburg Lens"
    models = []

    # if(cube_side_lenght>support_length):
    # # # Make the initial center cube
    #     cube = stl_gen.generate_prism(x_lenght=cube_side_lenght, y_lenght=cube_side_lenght,
    #                                 z_lenght=cube_side_lenght, xyz_position=cubic_center)
    #     models.append(cube)
    
    # Then make all the 6 joints
    models.append(stl_gen.generate_prism(x_lenght=support_side_length, y_lenght=support_length,
                  z_lenght=support_length, xyz_position=[cubic_center[0], cubic_center[1], cubic_center[2]]))
    models.append(stl_gen.generate_prism(x_lenght=support_length, y_lenght=support_length,
                  z_lenght=support_side_length, xyz_position=[cubic_center[0], cubic_center[1], cubic_center[2]]))
    models.append(stl_gen.generate_prism(x_lenght=support_length, y_lenght=support_side_length,
                  z_lenght=support_length, xyz_position=[cubic_center[0], cubic_center[1], cubic_center[2]]))

    unit_cell = stl_gen.merge_models(models=models)

    volume = calculate_mesh_volume(unit_cell)
    print("Volume of the mesh:", volume)

    # We manually calculate the volume of each cell
    get_cubic_unit_cell_ratios(support_length=support_length,
                               support_side_length=support_side_length, cube_side_lenght=cube_side_lenght)

    return unit_cell


def generate_sphere_unit_cell(sphere_center: list = [0, 0, 0], support_length: int = 0, sphere_radius: int = 0):
    # Unit cell based of the "A Highly Efficient Energy Harvesting Circuit Using Luneburg Lens"

    # Make the initial center sphere
    sphere = stl_gen.generate_sphere(
        radius=sphere_radius, resolution=2, center=sphere_center)
    models = [sphere]
    # Then make all the 6 joints
    models.append(stl_gen.generate_prism(L=support_length, A=support_length, xyz_position=[
                  sphere_center[0]+sphere_radius, sphere_center[1], sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length, A=support_length, xyz_position=[
                  sphere_center[0]-sphere_radius, sphere_center[1], sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length, A=support_length, xyz_position=[
                  sphere_center[0], sphere_center[1]+sphere_radius, sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length, A=support_length, xyz_position=[
                  sphere_center[0], sphere_center[1]-sphere_radius, sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length, A=support_length, xyz_position=[
                  sphere_center[0], sphere_center[1], sphere_center[2]+sphere_radius]))
    models.append(stl_gen.generate_prism(L=support_length, A=support_length, xyz_position=[
                  sphere_center[0], sphere_center[1], sphere_center[2]-sphere_radius]))

    unit_cell = stl_gen.merge_models(models=models)
    return unit_cell
