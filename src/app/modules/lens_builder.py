import numpy as np
import modules.geometry as geometry
import modules.stl_generator_pymesh as stl_gen
import modules.unit_cells as unit_cells
import modules.permitivity_solver as permitivity_solver


def build_cells(sphere_radius: float, epsilon: float, support_length: float):

    MIN_EPSILON = 1.2
    models = []
    half_models = []
    size = sphere_radius*2

    # We calulcate first the parameters of the cell structural integrety
    f2, f1 = permitivity_solver.get_ratio(
        epsilon1=1, epsilon2=epsilon, min_epsilon=MIN_EPSILON, sphere_radius=sphere_radius, center_distance=sphere_radius)

    support_side_length=unit_cells.calculate_support_side_length(f2_ratio=f2,support_length=support_length)
    
    print(f"{f2} {support_length} {support_side_length}")
    # for z in np.arange(-size/2, size/2, support_length):
    #     for y in np.arange(-size/2, size/2, support_length):
    #         for x in np.arange(-size/2, size/2, support_length):
    #             if geometry.check_point_in_sphere(point=[x, y, z], radius=sphere_radius):
    #                 center_distance = (x**2 + y**2 + z**2)**0.5
    #                 f2, f1 = permitivity_solver.get_ratio(
    #                     epsilon1=1, epsilon2=epsilon, min_epsilon=MIN_EPSILON, sphere_radius=sphere_radius, center_distance=center_distance)

    #                 cube_side_length_adjusted = cube_side_length * \
    #                     (1 - (((x**2 + y**2+z**2)) * 0.02))
    #                 if (cube_side_length_adjusted >= dielectric_ratio_length):
    #                     cube_side_length_adjusted = dielectric_ratio_length
    #                 model = unit_cells.generate_cubic_unit_cell(
    #                     cubic_center=[x, y, z],
    #                     support_length=support_length,
    #                     cube_side_lenght=cube_side_length_adjusted,
    #                     support_side_length=cube_side_length
    #                 )
    #                 models.append(model)
    #                 if x >= 0:
    #                     half_models.append(model)

    return models, half_models


def build_models(models: list, half_models: list, models_dir: str, filename: str):

    k = 10

    model = stl_gen.merge_models(models=models)
    model_scaled = stl_gen.scale_model(mesh=model, scale_factor=k)

    half_model = stl_gen.merge_models(models=half_models)
    half_model_scaled = stl_gen.scale_model(mesh=half_model, scale_factor=k)
    stl_gen.export_to_stl(
        mesh=model_scaled, filename=f"{models_dir}/{filename}.stl")
    stl_gen.export_to_stl(
        mesh=model_scaled, filename=f"{models_dir}/{filename}.obj")
    stl_gen.export_to_stl(mesh=half_model_scaled,
                          filename=f"{models_dir}/{filename}_cross.stl")
