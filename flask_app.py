from flask import Flask, request, jsonify
from functools import wraps
import jwt

app = Flask(__name__)

# Dummy secret key (replace it with your actual secret key)
SECRET_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBjuRJvdtKdcatBi+HsKGE4
PdMwMh6/lVmxyrY5LtKtOqfliXD3LMUd+EVOrd41s4tScwHiJ5kRV1enG8ypJ1PF
JQAHxejBHATgLCMauHx84rtikVuD5ICVwjJVcTJLJlCkg6/CKT0BCiYyjRPw62qB
LBhyVXwoaqfhM5BfD6kr6LXjEFRiE1JGmameKUkPhpRcLs+p6o8avMPwkUxp1HV8
5ptYlvONaUUak8uzu1liIMwgiN3uqMk6r2SByJ/scolIeH6CcrIVMS0SNU/zZGNI
EGqkNBhGi7m0aJ3egCiSlk4jSSKKx4Fh3mD9wOie+Jvw05XKe6MnbLDzB2h7QvGz
AgMBAAE=
-----END PUBLIC KEY-----
"""


def validate_bearer_token(token):
    try:
        # Decode the JWT token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['RS256'])
        print(decoded_token)
        # Check for additional validations (e.g., expiration, custom claims)
        # Add your validation logic here

        return True

    except jwt.ExpiredSignatureError:
        return False  # Token has expired
    except jwt.InvalidTokenError:
        return False  # Invalid token

def require_bearer_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the Bearer token from the Authorization header
        token = request.headers.get('Authorization')

        if not token:
            return jsonify(error='Bearer token is missing.'), 401

        # Extract the token value (assuming Bearer token format)
        token = token.replace('Bearer ', '')

        # Validate the Bearer token
        if not validate_bearer_token(token):
            return jsonify(error='Invalid or expired Bearer token.'), 401

        # Bearer token is valid, proceed with the original function
        return func(*args, **kwargs)

    return wrapper

# GET endpoint with Bearer token validation
@app.route('/hello', methods=['GET'])
@require_bearer_token
def hello():
    name = request.args.get("Name")
    return jsonify(message=f'Hello,{name}!')

# POST endpoint with Bearer token validation
@app.route('/helloagain', methods=['POST'])
@require_bearer_token
def hello_again():
    # Get data from the request
    data = request.get_json()

    # Check if 'name' is present in the request data
    if 'name' in data:
        return jsonify(message=f'Hello again, {data["name"]}!')
    else:
        return jsonify(error='Name not found in the request data.'), 400

if __name__ == '__main__':
    app.run(debug=True)
