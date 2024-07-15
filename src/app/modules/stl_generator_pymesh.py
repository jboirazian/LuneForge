import numpy as np
import pymesh
from functools import reduce

def add_square_holes(sphere:pymesh.Mesh,holes:list):
    """
    Add square holes to the Lunenburg lens, going through the entire object.

    Parameters:
    - vertices: 3D coordinates of lens vertices.
    - holes: List of dictionaries, each specifying a hole with keys 'size' and 'position'.
    - through_value: Value to set for the z-coordinate inside the hole.

    Returns:
    - Updated vertices after adding the square holes.
    """
    for hole in holes:
        hole_size = hole['size']
        hole_position = hole['position']

        x=hole_position[0]
        y=hole_position[1]
        z=hole_position[2]
        
        square_hole_mesh=generate_prism_xy(L=z,A=hole_size,xy_positon=[x,y])


        sphere=pymesh.boolean(sphere, square_hole_mesh, operation="difference")

    return sphere



def generate_sphere(radius, resolution=16,center=[0,0,0]):
    """
    Generate a 3D solid sphere using PyMesh.

    Args:
        radius (float): Radius of the sphere.
        center (list): Center of the sphere [x, y, z].
        refinement_order (int): Number of refinement steps.

    Returns:
        PyMesh.Mesh: The generated sphere mesh.
    """
    sphere = pymesh.generate_icosphere(radius, np.array(center), resolution)
    return pymesh.form_mesh(sphere.vertices, sphere.faces)


def generate_cylinder(L, R, resolution=100):
    """
    Generate a 3D cylinder using PyMesh.

    Args:
        L (float): Length of the cylinder.
        R (float): Radius of the cylinder.
        resolution (int): Number of triangles to approximate the cylinder surface.

    Returns:
        PyMesh.Mesh: The generated cylinder mesh.
    """
    # Create the cylinder
    cylinder = pymesh.generate_cylinder(R, L, resolution)
    
    return pymesh.form_mesh(cylinder.vertices, cylinder.faces)



def merge_models(models:list):
    return pymesh.merge_meshes(models)

def fuse_models(models:list):
    fused_models=models[0]
    with click.progressbar(length=len(models),show_pos=True) as bar:
        for model in models:
            fused_models=pymesh.boolean(fused_models, model, operation="union")
            bar.update(1)
        return fused_models

def intersect_models(models:list):
    intersection_models=models[0]
    with click.progressbar(length=len(models),show_pos=True) as bar:
        for model in models:
            intersection_models=pymesh.boolean(intersection_models, model, operation="intersection")
            bar.update(1)
        return intersection_models


def scale_model(mesh,scale_factor):
    # Get the vertices of the mesh
    vertices = mesh.vertices

    # Scale the vertices by multiplying them by the scaling factors
    scaled_vertices = vertices * [scale_factor, scale_factor, scale_factor]

    # Create a new mesh with the scaled vertices
    scaled_mesh = pymesh.form_mesh(scaled_vertices, mesh.faces)

    return scaled_mesh




def add_square_hole_to_mesh(mesh,A,L,xy_position):
    square_hole_mesh=generate_prism_xy(L=L,A=A,xy_positon=xy_position)
    mesh=pymesh.boolean(mesh, square_hole_mesh, operation="difference")
    return mesh


def generate_prism_xy(L, A, num_samples=1, subdiv_order=0, xy_positon=[0,0]):
    """
    Generate a 3D prism with a square face using PyMesh.

    Args:
        L (float): Length of the prism.
        A (float): Area of the square face.
        num_samples (int): Number of segments on each edge of the box.
        subdiv_order (int): The subdivision order.
        x (float): X-coordinate of the position.
        y (float): Y-coordinate of the position.

    Returns:
        PyMesh.Mesh: The generated prism mesh.
    """

    x,y=xy_positon

    # Calculate the side length of the square face
    side_length = A
    
    # Define the min and max corners of the box
    box_min = np.array([x - side_length / 2, y - side_length / 2,-L/2])
    box_max = np.array([x + side_length / 2, y + side_length / 2,L/2])
    
    # Create the prism
    prism = pymesh.generate_box_mesh(box_min, box_max, num_samples, subdiv_order)
    
    return prism


def generate_prism(x_lenght:float,y_lenght:float,z_lenght:float, num_samples=1, subdiv_order=0, xyz_position=[0, 0, 0]):
    """
    Generate a 3D prism with a square face using PyMesh.

    Args:
        L (float): Length of the prism.
        A (float): Area of the square face.
        num_samples (int): Number of segments on each edge of the box.
        subdiv_order (int): The subdivision order.
        xyz_position (list of float): Coordinates of the position [x, y, z].

    Returns:
        PyMesh.Mesh: The generated prism mesh.
    """
    
    x, y, z = xyz_position
    
    # Define the min and max corners of the box
    box_min = np.array([x - x_lenght / 2, y - y_lenght / 2, z - z_lenght / 2])
    box_max = np.array([x + x_lenght / 2, y + y_lenght / 2, z + z_lenght / 2])
    
    # Create the prism
    prism = pymesh.generate_box_mesh(box_min, box_max, num_samples, subdiv_order)
    
    return prism




def export_to_stl(mesh, filename):
    """
    Export a PyMesh mesh to an STL file.

    Args:
        mesh (PyMesh.Mesh): The mesh to export.
        filename (str): The name of the STL file.

    """
    pymesh.save_mesh(filename, mesh)



def cut_mesh_in_half(mesh, axis='x'):
    """
    Cuts a mesh in half along the specified axis (default is x-axis).
    
    Returns:
    - cut_mesh: The cut mesh object.
    """
    
    # Define the cutting plane direction based on the specified axis
    if axis == 'x':
        direction = np.array([1.0, 0.0, 0.0])
    elif axis == 'y':
        direction = np.array([0.0, 1.0, 0.0])
    elif axis == 'z':
        direction = np.array([0.0, 0.0, 1.0])
    else:
        raise ValueError("Invalid axis specified. Choose from 'x', 'y', or 'z'.")
    
    # Slice the mesh into 2 parts along the specified direction
    slices = pymesh.slice_mesh(mesh, direction, 2)

    return slices[0]