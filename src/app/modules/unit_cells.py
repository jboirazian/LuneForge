import modules.stl_generator_pymesh as stl_gen



def generate_cubic_unit_cell(cubic_center:list=[0,0,0],support_length:int=0,cube_side_lenght:float=0.0,support_side_length:float=0.0):
    ### Unit cell based of the "A Highly Efficient Energy Harvesting Circuit Using Luneburg Lens"

    ### Make the initial center cube
    cube=stl_gen.generate_prism(x_lenght=cube_side_lenght,y_lenght=cube_side_lenght,z_lenght=cube_side_lenght,xyz_position=cubic_center)
    models=[cube]
    ### Then make all the 6 joints
    models.append(stl_gen.generate_prism(x_lenght=support_side_length,y_lenght=support_length,z_lenght=support_length,xyz_position=[cubic_center[0],cubic_center[1],cubic_center[2]]))
    models.append(stl_gen.generate_prism(x_lenght=support_length,y_lenght=support_length,z_lenght=support_side_length,xyz_position=[cubic_center[0],cubic_center[1],cubic_center[2]]))
    models.append(stl_gen.generate_prism(x_lenght=support_length,y_lenght=support_side_length,z_lenght=support_length,xyz_position=[cubic_center[0],cubic_center[1],cubic_center[2]]))

    print(f"{cubic_center[0]},{cubic_center[1]},{cubic_center[2]},{cube_side_lenght},{(cubic_center[0]**2+cubic_center[1]**2+cubic_center[2]**2)/25}")
    unit_cell=stl_gen.merge_models(models=models)

    ## We manually calculate the volume of each cell
    support_structure_volume=(3*(support_length*(support_side_length**2))-support_side_length**3)
    cube_volume=(cube_side_lenght**3)
    unit_cell_max_volume=support_side_length**3
    print(f"Max Space volume: {unit_cell_max_volume} |Cube volume: {cube_volume} | Support only volume: {support_structure_volume} (ratio : {support_structure_volume/unit_cell_max_volume})")
    return unit_cell



def generate_sphere_unit_cell(sphere_center:list=[0,0,0],support_length:int=0,sphere_radius:int=0):
    ### Unit cell based of the "A Highly Efficient Energy Harvesting Circuit Using Luneburg Lens"

    ### Make the initial center sphere
    sphere= stl_gen.generate_sphere(radius=sphere_radius,resolution=2,center=sphere_center)
    models=[sphere]
    ### Then make all the 6 joints
    models.append(stl_gen.generate_prism(L=support_length,A=support_length,xyz_position=[sphere_center[0]+sphere_radius,sphere_center[1],sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length,A=support_length,xyz_position=[sphere_center[0]-sphere_radius,sphere_center[1],sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length,A=support_length,xyz_position=[sphere_center[0],sphere_center[1]+sphere_radius,sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length,A=support_length,xyz_position=[sphere_center[0],sphere_center[1]-sphere_radius,sphere_center[2]]))
    models.append(stl_gen.generate_prism(L=support_length,A=support_length,xyz_position=[sphere_center[0],sphere_center[1],sphere_center[2]+sphere_radius]))
    models.append(stl_gen.generate_prism(L=support_length,A=support_length,xyz_position=[sphere_center[0],sphere_center[1],sphere_center[2]-sphere_radius]))

    unit_cell=stl_gen.merge_models(models=models)
    return unit_cell