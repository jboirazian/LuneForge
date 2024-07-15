#/bin/bash

curl -X POST http://172.22.0.2:5000/generate_sphere_mesh -H "Content-Type: application/json" -d '{
    "scale_factor": 10,
    "cube_side_length": 0.5,
    "support_length": 0.2,
    "sphere_radius": 7
}'
