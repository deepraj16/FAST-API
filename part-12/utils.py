from passlib.context import CryptContext 


pwd_context = CryptContext(schemes=['bcrypt']) # here the bcrypt is an algo for working with to hash the values of give code 


def hashing(password):
    return pwd_context.hash(password)        

def verify(user_password,hashed_password): 
    return pwd_context.verify(user_password,hashed_password)  