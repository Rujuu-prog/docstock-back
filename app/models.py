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

    join_groups = relationship("Group", secondary="user_group_roles", back_populates="join_users", overlaps="user_roles,group_roles,role_users,role_groups")
    user_roles = relationship("Role", secondary="user_group_roles", back_populates="role_users", overlaps="join_groups,role_groups,group_roles,join_users")
    have_documents = relationship("Document", back_populates="owner_user")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    join_users = relationship("User", secondary="user_group_roles", back_populates="join_groups", overlaps="group_roles,role_users,role_groups,user_roles")
    group_roles = relationship("Role", secondary="user_group_roles", back_populates="role_groups", overlaps="join_users,role_users,user_roles,join_groups")
    inside_documents = relationship("Document", back_populates="owner_group")



class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    role_users = relationship("User", secondary="user_group_roles", back_populates="user_roles", overlaps="role_groups,join_users,group_roles,join_groups")
    role_groups = relationship("Group", secondary="user_group_roles", back_populates="group_roles", overlaps="role_users,join_users,user_roles,join_groups")



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
    owner_user = relationship("User", back_populates="have_documents")

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    owner_group = relationship("Group", back_populates="inside_documents")

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
