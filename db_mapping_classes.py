from sqlalchemy import Table, Column, Integer, Numeric, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Lecture(Base):
    __tablename__ = 'lecture'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    track_id = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    lecturer_id = Column(Integer, ForeignKey('lecturer.id'))

    lecturer = relationship("Lecturer", back_populates="lecturies")
    category = relationship("Category", back_populates="lecturies")

    def __init__(self, name, track_id, category_id, lecturer_id):
        self.name = name
        self.track_id = track_id
        self.category_id = category_id
        self.lecturer_id = lecturer_id

    def __repr__(self):
       return "<Lecture('%s','%s')>" % \
                    (self.name, self.lecturer_id)

    def __eq__(self, other):
        if self.track_id == other.track_id:
            return True
        else:
            return False

    # def __dict__(self):
    #     d = {}
    #     d['name'] = self.name
    #     d['track_id'] = self.track_id
    #     d['category'] = self.category
    #     d['lecturer'] = self.lecturer
    #     return d


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    lecturies = relationship("Lecture", back_populates="category")

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Category('%s', '%s')>" % \
               (self.name, self.description)

    def __eq__(self, other):
        if self.name == other.name and self.description == other.description:
            return True
        else:
            return False


class Lecturer(Base):
    __tablename__ = 'lecturer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lecturies = relationship("Lecture", back_populates="lecturer")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
       return "<Lecturer('%s')>" % \
                    (self.name)

    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False


    # def __dict__(self):
    #     d = {}
    #     d['name'] = self.name
    #     return d

class DBInit:

    def __init__(self):
        self.engine = create_engine('sqlite:///teachinbot.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_session(self):
        return self.session