from encrypt import encryptor
from extract import extractor
from flask import Flask, request, render_template, send_file
import os
import tempfile
import numpy as np
import PIL.Image

app = Flask(__name__)

temp_dir = tempfile.TemporaryDirectory()




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'imageUpload' not in request.files:
        return "No file part"
    
    file = request.files['imageUpload']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        temp_filename = os.path.join(temp_dir.name, file.filename)
        file.save(temp_filename)
    
        processed_image = encryptor(temp_filename, request.form['secretMessage'])
        
        os.remove(temp_filename)
        
        if processed_image is not None:
            processed_image_path = os.path.join(temp_dir.name, 'processed_image.png')
            processed_image.save(processed_image_path)
            return send_file(processed_image_path, as_attachment=True)
        else:
            return "Not enough space to hide the message"




@app.route('/extract', methods=['POST'])
def extract_message():
    if 'imageUpload' not in request.files:
        return "No file part"

    file = request.files['imageUpload']

    if file.filename == '':
        return "No selected file"

    if file:
        temp_filename = os.path.join(temp_dir.name, file.filename)
        file.save(temp_filename)

        extracted_message = extractor(temp_filename)

        os.remove(temp_filename)

        return render_template('hidden_msg.html', decoded_message=extracted_message)



if __name__ == '__main__':
    app.run(debug=True)
