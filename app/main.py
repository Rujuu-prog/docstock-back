from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils import is_valid_email, hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not is_valid_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")
    # Check if a user with the same name or email already exists
    db_user = crud.get_user_by_name_or_email(db, name=user.name, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the same name or email already exists")
    
    hashed_password = hash_password(user.password)
    db_user = models.User(name=user.name, password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.post("/groups/", response_model=schemas.Group)
async def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    # Check if creator_id exists
    db_user = crud.get_user(db=db, user_id=group.creator_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.create_group(db=db, group=group)

@app.get("/groups/{group_id}", response_model=schemas.Group)
async def get_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db=db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return db_group

@app.get("/roles/{role_id}", response_model=schemas.Role)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud.get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return db_role

@app.post("/documents/", response_model=schemas.Document)
async def create_document(document: schemas.DocumentCreate, owner_id: int, group_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=owner_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_group = crud.get_group(db=db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return crud.create_document(db=db, document=document, owner_id=owner_id, group_id=group_id)

@app.get("/documents/{document_id}", response_model=schemas.Document)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.get_document(db=db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return db_document

@app.post("/tags/", response_model=schemas.Tag)
async def create_tag(tag: schemas.TagCreate, document_id: int, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag, document_id=document_id)

@app.get("/tags/{tag_id}", response_model=schemas.Tag)
async def get_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return db_tag

@app.post("/user_group_roles/")
async def add_user_to_group(user_id: int, group_id: int, role_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_group = crud.get_group(db=db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    db_role = crud.get_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    user_group_role = crud.add_user_to_group(db=db, user_id=user_id, group_id=group_id, role_id=role_id)
    return user_group_role
