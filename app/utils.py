from passlib.context import CryptContext ##this will be used for hashing the passwords 

pwd_context= CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def hash(password: str):
    return pwd_context.hash(password)

##defining a function for hashing the attempted password by the user for login and then comparing it with the saved password from the signature (secret)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 
