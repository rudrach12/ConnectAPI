from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models
from app.schema import UserRegister,UserResponse,PostCreate,PostResponse

# This creates all tables in the database automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ConnectAPI", version="0.1.0")

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "message": "Server is running"}

@app.get("/", tags=["health"])
def root():
    return {"message": "Welcome to ConnectAPI"}

@app.post(
    "/users/register",
    response_model=UserResponse,
    status_code=201,
    tags=["users"],
    summary="Register a new user"
)
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    # Check if email exists in real DB
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user object
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)      # stage the insert
    db.commit()           # actually save to DB
    db.refresh(new_user)  # get the generated ID back

    return new_user

@app.get(
    "/users",
    response_model=list[UserResponse],
    status_code=200,
    tags=["users"],
    summary="Get all users"
)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=200,
    tags=["users"],
    summary="Get a single user by ID"
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.post(
    "/posts",
    response_model=PostResponse,
    status_code=201,
    tags=["posts"],
    summary="add new user chat"
)
def add_new_post(post:PostCreate, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==post.user_id).first()

    if not user:
        raise HTTPException(status_code=400,detail="Invalid User")
    
    new_post = models.Post(
        title = post.title,
        content = post.content,
        user_id = post.user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@app.get(
    "/posts",
    response_model=list[PostResponse],
    status_code=200,
    tags=["posts"],
    summary="getting all posts"
)
def get_all_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    return posts

@app.get(
    "/posts/{posts_id}",
    response_model=PostResponse,
    status_code=200,
    tags=["posts"],
    summary="getting a single post by id"
)
def get_post_by_id(posts_id:int,db:Session = Depends(get_db)):

    existing_post = db.query(models.Post).filter(posts_id==models.Post.id).first()

    if not existing_post:
        raise HTTPException(status_code=404,detail="Invalid Post id")

    return existing_post
