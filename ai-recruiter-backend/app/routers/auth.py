from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from ..services.database import db
from ..utils import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from ..models.auth import Token, UserCreate, UserResponse, TokenData
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    user = db.get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
        
    user_dict = dict(user)
    
    # Enrich with profile info (full_name)
    if user_dict["role"] == "candidate":
        candidate = db.get_candidate_by_user_id(user_dict["id"])
        if candidate:
            user_dict["full_name"] = candidate["full_name"]
    elif user_dict["role"] == "recruiter":
        company = db.get_company_by_user_id(user_dict["id"])
        if company:
            user_dict["full_name"] = company["name"]
            
    return user_dict

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        existing_user = db.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(user.password)
        user_id = db.create_user(user.email, hashed_password, user.role)
        
        # Auto-create profile based on role
        if user.role == "candidate":
            # Create empty candidate profile linked to user
            db.create_candidate(user_id=user_id, full_name=user.full_name or "New Candidate", email=user.email)
        elif user.role == "recruiter":
            # Create empty company profile linked to user
            db.create_company(user_id=user_id, name=user.company_name or "My Company")

        return {"id": user_id, "email": user.email, "role": user.role}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get_user_by_email(form_data.username) # OAuth2 form uses 'username' for email
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"], "id": user["id"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
