from flask import Flask, request, jsonify , render_template
import modules.stl_generator_pymesh as stl_gen
import numpy as np
import modules.unit_cells as unit_cells
import modules.geometry as geometry
import uuid

app = Flask(__name__, static_url_path='',static_folder='static',template_folder='templates')

@app.route('/render')
def render_model():
    try:
        model_uuid = request.args.get('model_uuid', default = "", type = str)
        return render_template("render.html",model1_id=f"{model_uuid}.stl",model2_id=f"{model_uuid}_cross.stl"), 200
    except Exception as e:
        app.logger.error(f"Error serving render.html: {e}")
        return jsonify({"error": "File not found"}), 404


@app.route('/')
def main_page():
    try:
        return app.send_static_file("index.html")
    except Exception as e:
        app.logger.error(f"Error serving index.html: {e}")
        return jsonify({"error": "File not found"}), 404



@app.route('/generate_sphere_mesh', methods=['POST'])
def generate_sphere_mesh():
    data = request.args
    filename = str(uuid.uuid4())
    k = data.get('scale_factor', 10)
    cube_side_length = data.get('cube_side_length', 0.5)
    support_length = data.get('support_length', 0.2)
    sphere_radius = data.get('sphere_radius', 7)
    
    size = sphere_radius * 2
    models = []
    half_models = []

    for z in np.arange(-size/2, size/2, cube_side_length):
        for y in np.arange(-size/2, size/2, cube_side_length):
            for x in np.arange(-size/2, size/2, cube_side_length):
                if geometry.check_point_in_sphere(point=[x, y, z], radius=sphere_radius):
                    cube_side_length_adjusted = cube_side_length * (1 - (((x**2 + y**2+z**2)) * 0.02))
                    model = unit_cells.generate_cubic_unit_cell(
                        cubic_center=[x , y , z ],
                        support_length=support_length,
                        cube_side_lenght=cube_side_length_adjusted,
                        support_side_length=cube_side_length
                    )
                    models.append(model)
                    if x >= 0:
                        half_models.append(model)
                        if x == 0 and y == 0 and z == 0:
                            stl_gen.export_to_stl(mesh=model, filename=f"static/{filename}_unit_cell_000.stl")
                        if x == 0 and z == 0:
                            print(f"#;{x};{y};{cube_side_length_adjusted};{sum(model.get_attribute('voxel_volume'))}")

    model = stl_gen.merge_models(models=models)
    model_scaled = stl_gen.scale_model(mesh=model, scale_factor=k)
    stl_gen.export_to_stl(mesh=model_scaled, filename=f"static/{filename}.stl")

    half_model = stl_gen.merge_models(models=half_models)
    half_model_scaled = stl_gen.scale_model(mesh=half_model, scale_factor=k)
    stl_gen.export_to_stl(mesh=half_model_scaled, filename=f"static/{filename}_cross.stl")

    stl_gen.export_to_stl(mesh=models[round(len(models)/3)], filename=f"static/{filename}_unit_cell_center.stl")
    stl_gen.export_to_stl(mesh=models[0], filename=f"static/{filename}_unit_cell_periphery.stl")

    html_button=f'''<button class="btn btn-secondary" href='/render?model_uuid={filename}'>View</button>'''

    return html_button

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
