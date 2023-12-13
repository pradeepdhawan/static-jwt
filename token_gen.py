import jwt
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Generate a public-private key pair
private_key_str = """
-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQBjuRJvdtKdcatBi+HsKGE4PdMwMh6/lVmxyrY5LtKtOqfliXD3
LMUd+EVOrd41s4tScwHiJ5kRV1enG8ypJ1PFJQAHxejBHATgLCMauHx84rtikVuD
5ICVwjJVcTJLJlCkg6/CKT0BCiYyjRPw62qBLBhyVXwoaqfhM5BfD6kr6LXjEFRi
E1JGmameKUkPhpRcLs+p6o8avMPwkUxp1HV85ptYlvONaUUak8uzu1liIMwgiN3u
qMk6r2SByJ/scolIeH6CcrIVMS0SNU/zZGNIEGqkNBhGi7m0aJ3egCiSlk4jSSKK
x4Fh3mD9wOie+Jvw05XKe6MnbLDzB2h7QvGzAgMBAAECggEAXuPnN+swBCL6W5eY
dZgC0np5731xpsmdnMEQXh9A1xdeVdtPg9O1CYyJnpFxRVZAN0c6PpGBZG/g9yFL
wJWsb4aCneLjVIWt2gYFrVJpGojA180K8NjIxjgQnx7kRYAC8lhgMPf+lXOr3yRB
GllYceuco4bWarr6Xh8rvFjxl9ZToJPnKWps37sX7dktD1E0hfM2r/GDF0KhyXTs
4GXZwH9WPdoZaKA5rBpeyG/BKyBM89T9CpQ/AcKO85+wCkPEp+CRhK5aFT0cjmmx
IsiKrtfWfFvfyGkqaeYE+AKOC4x3jbPY6mFpI7YlV54UmPCKTS1Tc0cjqK2Cy4FL
qU2m6QKBgQDGg1iqP4l5fQk5KawfznNHG7YrJ2CK8wbwUx1QT9ivpeB/yV+BRsHo
NUpU7QSGdGtBPknWw6SxxPAQ3uTtWIMpK+H3PgETFrfdSAcgFpXfp/Tf40xiqoiF
7sYmOYVFrbDFzvF39om+RoagtByDwEqHSsourWN7kLXIvw4Z60Py3wKBgQCAmfmq
/dgq20Ho16Gn+CWMupRVTQDY54cW6xUObwW6JahB2vzYNzhQVBi4WjSFQYFXY3OI
ezy8ZVUuedTXrRaFtCxQkt1aW6KIOZWb/mmg8VNQHXQrgfDoCUTbzztiyPBGdkLw
62ZotADP/aJKk49GV6N0Ez5k6XLVdonFEztPrQKBgG5O1DkeP0UL7tEdz/CIptQP
mQWXxvTPIL7wYGydQdowwXQgsPpEGEHxQtG4NviDvomtlBhL9Lt3pLKrOOiOc6uw
H8tkX/J8gETs3lC9XCDA0riKNIrrGhvaV68r7VuPrZfta45up5Hc3Lh1/RZVBtTx
ATI41Pv3qJvZVnuemM5fAoGAartgM0IqvqbqtM0CJd4VjA7uPT2DjoHZ5HOHLkuG
fU/zrXSKlQh/fGvPeHGlVVNgfZ7UrFlbtyCC6efDdpz5LE602MqLXArhgh4IxUcJ
c8HWW4+WcuWNg4bt12DO8NXEVTahqEI25H9AjV776tk8+CyURCoUhrwZyoBvJ1km
yKECgYAcSljSdnz9tqEIwmOP1ymAFa/1IBZkjJaW/QQVf3SYPQN29RBD3TOAJEbm
LLqyxpTiXEV9zz75KaiUF9F78KSyUa0cfktCtU7LRTF+C3T9BWJdTYwHjtRPyMv4
LNnyjcbTl+CMNS9x4C2FdA4+SUgLPNXVA2HnRYhaBx0Av/gQuQ==
-----END RSA PRIVATE KEY-----
"""

public_key_str = """
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

# Convert the private key string to an RSA private key object
private_key = serialization.load_pem_private_key(
    private_key_str.encode('utf-8'),
    password=None,
    backend=default_backend()
)

# Set the expiration to a distant future timestamp
expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=36500)  # 100 years from now

# Payload for the JWT token
payload = {
    "user_id": "UWP Service",
    "description": "static secret key that will expire in 100 years as Alexis's requirement",
    "exp": expiration_time
}

# Generate the JWT token using RS256 algorithm
token = jwt.encode(payload, private_key, algorithm='RS256')

# Decode the JWT token using the public key
decoded_payload = jwt.decode(token, public_key_str, algorithms=['RS256'])
print("JWT Token:", token)
print("Decoded Payload:", decoded_payload)
