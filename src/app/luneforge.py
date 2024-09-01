from flask import Flask, request, jsonify, render_template
import modules.stl_generator_pymesh as stl_gen
import numpy as np
import modules.unit_cells as unit_cells
import modules.geometry as geometry
import uuid
from os import listdir, stat
from os.path import isfile, join, getctime
import datetime
import json

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')


models_dir=f"{app.static_folder}/models"


@app.route('/render')
def render_model():
    try:
        model_uuid = request.args.get('model_uuid', default="", type=str)
        return render_template("render.html", cst_studio_model_id=f"models/{model_uuid}.obj", model1_id=f"models/{model_uuid}.stl", model2_id=f"models/{model_uuid}_cross.stl"), 200
    except Exception as e:
        app.logger.error(f"Error serving render.html: {e}")
        return jsonify({"error": "File not found"}), 404


@app.route('/builds')
def show_builds():
    try:
        return render_template("builds.html"), 200
    except Exception as e:
        app.logger.error(f"Error serving builds.html: {e}")
        return jsonify({"error": "File not found"}), 404


@app.route('/get_builds')
def get_builds():
    try:

        files = [f for f in listdir(models_dir) if isfile(
            join(models_dir, f))]
        html_data = ""
        for file in files:
            if ((".stl" in file) and ('_' not in file)):
                id=file.replace(".stl", "")
                creation_time = getctime(f"{models_dir}/{file}")
                creation_date = datetime.datetime.fromtimestamp(creation_time)
                info = json.load( open( f"{models_dir}/{id}.json" ) )
                html_data += render_template("containers.html", filename=id, creation_date=creation_date,info=info)
        return html_data, 200
    except Exception as e:
        app.logger.error(f"Error: {e}")
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
    data = request.form
    print(data)
    filename = str(uuid.uuid4())
    k = data.get('scale_factor', type=float)
    cube_side_length = data.get('cube_side_length', type=float)
    support_length = data.get('support_length', type=float)
    sphere_radius = data.get('sphere_radius', type=float)

    size = sphere_radius * 2
    models = []
    half_models = []

    for z in np.arange(-size/2, size/2, cube_side_length):
        for y in np.arange(-size/2, size/2, cube_side_length):
            for x in np.arange(-size/2, size/2, cube_side_length):
                if geometry.check_point_in_sphere(point=[x, y, z], radius=sphere_radius):
                    cube_side_length_adjusted = cube_side_length * \
                        (1 - (((x**2 + y**2+z**2)) * 0.02))
                    model = unit_cells.generate_cubic_unit_cell(
                        cubic_center=[x, y, z],
                        support_length=support_length,
                        cube_side_lenght=cube_side_length_adjusted,
                        support_side_length=cube_side_length
                    )
                    models.append(model)
                    if x >= 0:
                        half_models.append(model)

    model = stl_gen.merge_models(models=models)
    model_scaled = stl_gen.scale_model(mesh=model, scale_factor=k)

    half_model = stl_gen.merge_models(models=half_models)
    half_model_scaled = stl_gen.scale_model(mesh=half_model, scale_factor=k)
    stl_gen.export_to_stl(mesh=model_scaled, filename=f"{models_dir}/{filename}.stl")
    stl_gen.export_to_stl(mesh=model_scaled, filename=f"{models_dir}/{filename}.obj")
    stl_gen.export_to_stl(mesh=half_model_scaled,
                          filename=f"{models_dir}/{filename}_cross.stl")

    # Save metadata of file
    data = {"id": filename, "k": k, "cube_side_length": cube_side_length,
            "support_length": support_length, "sphere_radius": sphere_radius}

    stl_gen.generate_metadata(path=models_dir,data=data)

    html_button = f'''<button class="btn btn-secondary" onclick="location.href='/render?model_uuid={filename}'">View</button>'''

    return html_button


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
