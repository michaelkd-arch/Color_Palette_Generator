import os.path

from flask import Flask, render_template, request
from datetime import datetime
from colorthief import ColorThief
import numpy as np
from PIL import Image

CURRENT_YEAR = datetime.now().year
ALLOWED_EXTENSIONS = {'jpg', 'png'}


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html', current_year=CURRENT_YEAR,)


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file and allowed_file(uploaded_file.filename):
        destination = os.path.join('uploads/', f'file.{uploaded_file.filename.rsplit(".", 1)[1]}')
        uploaded_file.save(destination)
        ct = ColorThief(destination)
        color_palette = ct.get_palette(color_count=17)
        my_array = np.reshape(color_palette, (4, 4, 3))
        im = Image.fromarray(my_array.astype(np.uint8)).resize((1600, 1600), resample=Image.NEAREST)
        palette_path = os.path.join("static/img/", "palette.png")
        im = im.save(palette_path)
        palette_hex = ['#%02x%02x%02x' % t for t in color_palette]
        return render_template('index.html', current_year=CURRENT_YEAR, palette=palette_hex)
    else:
        return {'error': 'File Upload Failed'}, {'Refresh': '2; url=http://127.0.0.1:5003/'}


if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')
