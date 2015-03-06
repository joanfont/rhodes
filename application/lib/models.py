from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
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


class DictMixin(object):

    def to_dict(self):
        raise NotImplementedError()


class Person(DictMixin, Base):

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


class Teacher(Person):
    pass


class Student(Person):
    pass


class Message(DictMixin, Base):

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


class Course(DictMixin, Base):

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

teacher_subject = Table(
    'teacher_subject',
    Base.metadata,
    Column('teacher', Integer, ForeignKey('person.id')),
    Column('subject', Integer, ForeignKey('subject.id')),
)


class Subject(DictMixin, Base):

    __tablename__ = 'subject'

    # Id field could be replaced by code field
    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String(60))
    teachers = relationship('Teacher', backref='subjects', secondary=teacher_subject)

    @property
    def group_list(self):
        return map(lambda x: x.to_dict(), self.groups)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'groups': self.group_list,
        }


student_group = Table(
    'student_group',
    Base.metadata,
    Column('student', Integer, ForeignKey('person.id')),
    Column('group', Integer, ForeignKey('group.id')),
)


class Group(DictMixin, Base):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(
        Subject,
        backref=backref('groups', uselist=True, cascade='delete,all'))

    students = relationship('Student', backref='subjects', secondary=student_group)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
