from flask import Flask, request, render_template, jsonify
from google.cloud import storage
import google.auth
from google.auth.transport.requests import AuthorizedSession
import os
import os, urllib
import google.auth.transport.requests
import google.oauth2.id_token

app = Flask(__name__)

# Set up Google Cloud Storage client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds\main-bloom-407506-00633c3d5b96.json'
client = storage.Client()
bucket = client.get_bucket('call-summarization-input')

# Set up Google Cloud authentication
credentials, project = google.auth.load_credentials_from_file(
    'creds\main-bloom-407506-00633c3d5b96.json', scopes=['https://www.googleapis.com/auth/cloud-storage', 'https://www.googleapis.com/auth/cloud-platform'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def serve_favicon():
    return app.send_static_file('favicon.ico')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the file from form data
    file = request.files['audio_file']
    print("File: ")
    print(file)
    # Make sure a file was submitted
    if not file:
        return "No file provided..."
    
    # Create a blob 
    blob = bucket.blob(file.filename)
    status = blob.upload_from_string(file.read(), content_type=file.content_type)
    return jsonify({'transcript': 'Test Transcript', 'summary': 'Test Summary', 'sentiment': 'Test Sentiment'})

@app.route('/call_cloud_function')
def call_cloud_function():

    cloud_function_url = 'https://us-central1-main-bloom-407506.cloudfunctions.net/trigger_job'
    
    req = urllib.request.Request(cloud_function_url)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, cloud_function_url)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)

    return response

if __name__ == '__main__':
    app.run(debug=True)