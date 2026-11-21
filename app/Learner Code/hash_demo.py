from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

# Hash a password (automatically generates a random salt)
hashed = ph.hash("correct horse battery staple")
print(hashed)

# Verify a password (returns True or raises VerifyMismatchError)
try:
    ph.verify(hashed, "correct horse battery staple")
    print("Password matches!")
except VerifyMismatchError:
    print("Invalid password.")
    
    
