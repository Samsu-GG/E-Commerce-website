from fastapi.security import OAuth2PasswordBearer

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/signin")