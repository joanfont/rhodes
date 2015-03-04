from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Date, DateTime, ForeignKey

dsn = 'mysql://root:@localhost/rhodes'
db = create_engine(dsn)

Base = declarative_base()


class SessionWrapper(object):
    def __init__(self):
        self.session = sessionmaker(bind=db)()

    def add(self, obj):
        self.session.add(obj)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def query(self, cls):
        return self.session.query(cls)


class BaseModel(Base):

    def to_dict(self):
        raise NotImplementedError()


class Message(BaseModel):

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender = Column(Integer, ForeignKey('person.id'))

    message = Column(String(400))

    created_at = Column(DateTime)


    def __str__(self):
        return '<Message id={id}>'.format(id=self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
        }


class Person(BaseModel):

    __tablename__ = 'person'

    # Id field could be replaced by DNI field
    id = Column(Integer, primary_key=True)
    dni = Column(String(15), unique=True)
    first_name = Column(String(60))
    last_name = Column(String(120))
    email = Column(String(120))

    def to_dict(self):
        return {
            'id': self.id,
            'dni': self.dni,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }


class Course(BaseModel):

    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    starts_at = Column(Date)
    ends_at = Column(Date)

    def to_dict(self):
        return {
            'id': self.id,
            'starts_at': self.starts_at,
            'ends_at': self.ends_at,
        }


class Subject(BaseModel):

    __tablename__ = 'subject'

    # Id field could be replaced by code field
    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String(60))

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
        }

subject_students = Table(
    'subject_students',
    Base.metadata,
    Column('student', Integer, ForeignKey('person.id')),
    Column('subject', Integer, ForeignKey('subject.id')),
)


class Group(BaseModel):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    teacher = Column(Integer, ForeignKey('person.id'))
    students = relationship('Person', backref='subjects', secondary=subject_students)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'teacher': self.teacher,
            'students': self.students
        }

