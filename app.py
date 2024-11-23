import os
import yaml
from flask import Flask

# Load configuration from YAML file
with open("appconfig.yaml", 'r') as file:
    config = yaml.safe_load(file)

app = Flask(__name__)

# Access configuration values
port = config['server']['port']
auth_server_base_url = config['api']['auth-server']['base-url']

@app.route('/')
def health_check():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))
