from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    groups = relationship("Group", secondary="user_group_roles", backref="users")
    roles = relationship("Role", secondary="user_group_roles", backref="users")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    users = relationship("User", secondary="user_group_roles", backref="groups")
    roles = relationship("Role", secondary="user_group_roles", backref="groups")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    users = relationship("User", secondary="user_group_roles", backref="roles")
    groups = relationship("Group", secondary="user_group_roles", backref="roles")


class UserGroupRole(Base):
    __tablename__ = "user_group_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)

    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="documents")

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    groups = relationship("Group", back_populates="documents")

    tags = relationship("Tag", secondary="document_tags", back_populates="documents")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)

    documents = relationship("Document", secondary="document_tags", back_populates="tags")


class DocumentTag(Base):
    __tablename__ = "document_tags"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
