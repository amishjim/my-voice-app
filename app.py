from flask import Flask, render_template, request, jsonify, send_file
import os
import extract_voice

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
OUTPUT_FILE = 'My_Voice_Master.txt'

# Ensure the output file exists or is created in the current directory
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'w') as f:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # Get all uploaded files (not just specific names)
    uploaded_files = request.files.getlist('files')
    
    if not uploaded_files or len(uploaded_files) == 0:
        return jsonify({'error': 'No files uploaded'}), 400
    
    # Filter for JSON files only
    json_files = [f for f in uploaded_files if f.filename.endswith('.json')]
    
    if len(json_files) == 0:
        return jsonify({'error': 'No JSON files found'}), 400

    lyrics_only = request.form.get('lyrics_only') == 'true'

    # Save all JSON files
    saved_paths = []
    for json_file in json_files:
        if json_file.filename != '':
            file_path = os.path.join(UPLOAD_FOLDER, json_file.filename)
            json_file.save(file_path)
            saved_paths.append(file_path)
    
    # Process all files
    success, message = extract_voice.process_data(saved_paths, OUTPUT_FILE, lyrics_only)
    
    if success:
        return jsonify({'message': message, 'download_url': '/download'})
    else:
        return jsonify({'error': message}), 500

@app.route('/download')
def download_file():
    try:
        return send_file(OUTPUT_FILE, as_attachment=True)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
