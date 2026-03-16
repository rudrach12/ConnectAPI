from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models
from app.schema import UserRegister,UserResponse,PostCreate,PostResponse,FollowCreate,FollowResponse

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
    summary="Create a new post"
)
def add_new_post(post:PostCreate, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==post.user_id).first()

    if not user:
        raise HTTPException(status_code=404,detail="Invalid User")
    
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

@app.get(
    "/users/{user_id}/followers",
    response_model = list[FollowResponse],
    status_code = 200,
    tags = ["follows"],
    summary = "getting all the followers of a personn"
)
def get_all_followers(user_id:int ,db:Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(user_id==models.User.id).first()

    if not existing_user:
        raise HTTPException(status_code = 404,detail = "Invalid user id")
    
    all_followers = db.query(models.Follow).filter(user_id==models.Follow.following_id).all()

    return all_followers



@app.post(
    "/users/{user_id}/follow",
    response_model=FollowResponse,
    status_code=201,
    tags=["follows"],
    summary="Follow a user"
)
def follow_user(user_id: int, follow: FollowCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    target_user = db.query(models.User).filter(
        models.User.id == follow.following_id
    ).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User to follow not found")

    if user_id == follow.following_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    already_following = db.query(models.Follow).filter(
        models.Follow.follower_id == user_id,
        models.Follow.following_id == follow.following_id
    ).first()

    if already_following:
        raise HTTPException(status_code=400, detail="Already following this user")

    new_follow = models.Follow(
        follower_id=user_id,
        following_id=follow.following_id
    )
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return new_follow



@app.delete(
    "/users/{user_id}/unfollow/{unfollow_id}",
    status_code = 200,
    tags = ["follows"],
    summary = "Unfollowing the user"
)
def unfollow_user(user_id:int ,unfollow_id:int , db:Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(user_id==models.User.id).first()

    unfollowing_user = db.query(models.User).filter(unfollow_id == models.User.id).first()


    if not existing_user:
        raise HTTPException(status_code = 404,detail = "Invalid user id")
    
    if not unfollowing_user:
        raise HTTPException(status_code = 404,detail = "Invalid Follower id")

    
    follow = db.query(models.Follow).filter(
        (unfollow_id==models.Follow.following_id),
        (user_id==models.Follow.follower_id)).first()  
    
    if not follow:
        raise HTTPException(status_code = 404, detail="Not following this User")

    db.delete(follow)

    db.commit()

    return "Unfollow Successfully"
