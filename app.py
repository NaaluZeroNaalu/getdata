from flask import Flask, request, jsonify
import ibm_boto3
from ibm_botocore.client import Config
import os

# IBM Cloud Object Storage Configuration
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"  # Replace with your endpoint
COS_API_KEY_ID = "W9K3JjcK-DjSGtE_BlWIYm2JG6324FcpFE4dou0Nc08A"  # Replace with your API key
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/8471af1899b34564b2b04be799f50d75:57639010-98ef-4645-9923-1e5fa933f5a4::"
BUCKET_NAME = "srihari1"  # Replace with your bucket name

# Initialize IBM COS client
cos = ibm_boto3.client('s3',
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version='oauth'),
    endpoint_url=COS_ENDPOINT
)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If no file is selected, return an error
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file locally before uploading
    local_file_path = os.path.join("uploads", file.filename)  # Save to a folder named 'uploads'
    
    try:
        # Save the file locally
        file.save(local_file_path)
        
        # Upload the file to IBM COS
        with open(local_file_path, 'rb') as file_data:
            cos.upload_fileobj(file_data, BUCKET_NAME, file.filename)
        
        # Clean up the local file after upload (optional)
        os.remove(local_file_path)
        
        return jsonify({"message": f"File {file.filename} uploaded successfully to {BUCKET_NAME}."}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error uploading file: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
