from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import MappedColumn, mapped_column, relationship
from typing import Optional

from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    name: MappedColumn[str] = mapped_column(String(30))
    email: MappedColumn[str] = mapped_column(String(100), unique=True)
    password: MappedColumn[str] = mapped_column(String(200))

    template = relationship("Template", back_populates="user", cascade="all, delete-orphan")

class Template(db.Model):
    __tablename__ = 'template'
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey('user.id'))
    name: MappedColumn[str] = mapped_column(String(30))
    description: MappedColumn[str] = mapped_column(String(200))
    task_count: MappedColumn[Optional[int]] = mapped_column(Integer, default=0)

    user = relationship('User', back_populates='template')
    task = relationship('Task', back_populates='template', cascade="all, delete-orphan")


class Task(db.Model):
    __tablename__ = 'task'
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    template_id: MappedColumn[int] = mapped_column(Integer, ForeignKey('template.id'))
    name: MappedColumn[str] = mapped_column(String(100))
    description: MappedColumn[str] = mapped_column(String(200))
    start_date: MappedColumn[datetime] = mapped_column(DateTime, default=datetime.now)
    end_date: MappedColumn[Optional[datetime]] = mapped_column(DateTime)
    status: MappedColumn[Optional[int]] = mapped_column(Integer, default=0)

    template = relationship('Template', back_populates='task')



