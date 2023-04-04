from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name_or_email(db: Session, name: str, email: str):
    return db.query(models.User).filter((models.User.name == name) | (models.User.email == email)).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, password=user.password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def create_user_group_role(db: Session, user_id: int, group_id: int, role_id: int) -> models.UserGroupRole:
    """Create a new UserGroupRole."""
    user_group_role = models.UserGroupRole(user_id=user_id, group_id=group_id, role_id=role_id)
    db.add(user_group_role)
    db.commit()
    db.refresh(user_group_role)
    return user_group_role

def create_group(db: Session, group: schemas.GroupCreate) -> models.Group:
    """Create a new group."""
    db_group = models.Group(name=group.name, description=group.description)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def create_document(db: Session, document: schemas.DocumentCreate, owner_id: int, group_id: int):
    db_document = models.Document(title=document.title, content=document.content, owner_id=owner_id, group_id=group_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

def create_tag(db: Session, tag: schemas.TagCreate, document_id: int):
    new_tag = models.Tag(name=tag.name)
    db.add(new_tag)
    db.flush()

    document_tag = models.DocumentTag(document_id=document_id, tag_id=new_tag.id)
    db.add(document_tag)
    db.commit()

    return new_tag

def add_user_to_group(db: Session, user_id: int, group_id: int, role_id: int):
    user_group_role = models.UserGroupRole(user_id=user_id, group_id=group_id, role_id=role_id)
    db.add(user_group_role)
    db.commit()
    db.refresh(user_group_role)
    return user_group_role
