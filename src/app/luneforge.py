from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import modules.stl_generator_pymesh as stl_gen
import modules.lens_builder as lens_builder
from modules.release_info import show_release_info
import numpy as np
import modules.unit_cells as unit_cells
import modules.geometry as geometry
import uuid
from os import listdir, stat
from os.path import isfile, join, getctime
import datetime
import json
import markdown

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')


models_dir = f"{app.static_folder}/models"



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/render')
def render_model():
    try:
        model_uuid = request.args.get('model_uuid', default="", type=str)
        return render_template("render.html", cst_studio_model_id=f"models/{model_uuid}.obj", model1_id=f"models/{model_uuid}.stl", model2_id=f"models/{model_uuid}_cross.stl"), 200
    except Exception as e:
        app.logger.error(f"Error serving render.html: {e}")
        return jsonify({"error": "File not found"}), 404


@app.route('/docs')
def show_docs():
    try:
        return render_template("documentation.html"), 200
    except Exception as e:
        app.logger.error(f"Error serving documentation.html: {e}")
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
        if (len(files) == 0):
            # No files in directory
            html_data = render_template("no_builds.html")
            return html_data, 200

        for file in files:
            if ((".stl" in file) and ('_' not in file)):
                id = file.replace(".stl", "")
                creation_time = getctime(f"{models_dir}/{file}")
                creation_date = datetime.datetime.fromtimestamp(creation_time)
                info = json.load(open(f"{models_dir}/{id}.json"))
                html_data += render_template("containers.html",
                                             filename=id, creation_date=creation_date, info=info)
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


@app.route('/get_docs')
def documentation_page():
    try:
        with open(f"{app.static_folder}/docs/Docs.md", 'r', encoding='utf-8') as file:
            text = file.read()
            html_docs = markdown.markdown(text)
        return html_docs, 200
    except Exception as e:
        app.logger.error(f"Error serving docs/Docs.md: {e}")
        return jsonify({"error": "File not found"}), 404


@app.route('/generate_sphere_mesh', methods=['POST'])
def generate_sphere_mesh():
    try:
        data = request.form
        filename = str(uuid.uuid4())
        material=data.get('material', type=str)
        epsilon=float(material.split(";")[0])
        tan_loss=float(material.split(";")[-1])
        cube_side_length = data.get('cube_side_length', type=float)
        support_length = data.get('support_length', type=float)
        sphere_radius = data.get('sphere_radius', type=float)

        models, half_models = lens_builder.build_cells(sphere_radius=sphere_radius,support_length=support_length,epsilon=epsilon)

        lens_builder.build_models(
            models=models, half_models=half_models, models_dir=models_dir, filename=filename)
        # Save metadata of file
        data = {"id": filename, "cube_side_length": cube_side_length,
                "support_length": support_length, "sphere_radius": sphere_radius, "n_cells": len(models)}

        stl_gen.generate_metadata(path=models_dir, data=data)

        html_button = f'''<button class="btn btn-success w-full" onclick="location.href='/render?model_uuid={filename}'">View</button>'''
        return html_button
    except Exception as e:
        error_html = f'''<div class="collapse bg-error text-black"><input type="checkbox" /><div class="collapse-title text-xl font-medium">Error : Click to view</div><div class="collapse-content"><p>{e}</p></div></div>'''
        return error_html


if __name__ == "__main__":
    show_release_info()
    app.run(host='0.0.0.0', threaded=True, port=5000, debug=False)
