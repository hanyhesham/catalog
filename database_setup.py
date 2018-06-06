#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    email = Column(String(300), nullable=False)
    # picture = Column(String(300))


class Categories(Base):

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name}


class CategoryItem(Base):

    __tablename__ = 'category_item'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    description = Column(String(350))
    categories_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories, cascade='all, delete-orphan',
                              single_parent=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name,
                'description': self.description}


engine = create_engine('postgresql://catalog:password@localhost/catalog')

Base.metadata.create_all(engine)
