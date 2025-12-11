"""Authentication models."""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class User(BaseModel):
    """User model for authentication."""
    
    __tablename__ = "users"
    
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    role_assignments = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    approved_versions = relationship("LessonVersion", foreign_keys="LessonVersion.approved_by", back_populates="approver")
    resolved_escalations = relationship("EscalationRequest", foreign_keys="EscalationRequest.resolved_by", back_populates="resolver")
    audit_logs = relationship("AuditLog", foreign_keys="AuditLog.user_id", back_populates="user")


class Role(BaseModel):
    """Role model."""
    
    __tablename__ = "roles"
    
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    permissions = Column(String, nullable=True)  # JSON string or comma-separated
    
    # Relationships
    user_assignments = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")


class UserRole(BaseModel):
    """User-Role association model."""
    
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="role_assignments")
    role = relationship("Role", back_populates="user_assignments")

