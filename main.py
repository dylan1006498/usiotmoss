from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = 'your-api-key'
API_SECRET = 'your-secret-key'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    # Authenticate with Copyleaks API
    auth_url = 'https://id.copyleaks.com/v3/account/login/api'
    auth_response = requests.post(auth_url, json={'key': API_KEY, 'secret': API_SECRET})
    auth_response.raise_for_status()
    auth_token = auth_response.json()['access_token']

    # Submit file for scanning
    with open(file_path, 'rb') as f:
        scan_url = 'https://api.copyleaks.com/v3/education/submit/file'
        headers = {'Authorization': f'Bearer {auth_token}'}
        files = {'file': f}
        scan_response = requests.post(scan_url, headers=headers, files=files)

    os.remove(file_path)  # Clean up uploaded file
    return jsonify(scan_response.json())

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
