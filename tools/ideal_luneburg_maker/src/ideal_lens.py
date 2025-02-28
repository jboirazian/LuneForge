import sys
import modules.stl_generator_pymesh as stl_gen
import numpy as np
import pymesh
import os
import glob

# Luneburg equation for required permittivity at radius R
def luneburg_eq(Ro, R):
    return 2 - ((Ro ** 2) / (R ** 2))


if __name__ == "__main__":
    if(len(sys.argv)!=3):
        print(f"INVALID PARAMETERS RUN : {sys.argv[0]} [Lens_radious] [Layer_resoltion]")
        sys.exit(-1)
    R=float(sys.argv[1])
    RESOLUTION=int(sys.argv[2])
    DELTA=R/RESOLUTION
    LAYER=0
    print(f"Lens_radious: {R} | Layer_resoltion: {RESOLUTION}")
    for Ro in np.linspace(0,R, RESOLUTION):
        epsilon=luneburg_eq(Ro=Ro,R=R)
        if(Ro>0):
            solid_sphere=stl_gen.generate_sphere(radius=Ro,resolution=5)
            if(LAYER!=0):
                hollow_sphere=stl_gen.generate_sphere(radius=Ro-DELTA,resolution=5)
                shell_sphere=pymesh.boolean(solid_sphere, hollow_sphere, operation="difference")
            else:
                shell_sphere=solid_sphere
            print(f"models/{LAYER}_Ep_{epsilon}-Ro_{Ro}.obj")
            stl_gen.export_to_stl(mesh=shell_sphere,filename=f"models/{LAYER}_Ep_{epsilon}-Ro_{Ro}.obj")
            LAYER+=1

