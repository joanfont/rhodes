from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey

from config.rhodes import DB_DSN

db = create_engine(DB_DSN)

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

    def query(self, *args):
        return self.session.query(*args)


class DictMixin(object):

    def to_dict(self):
        raise NotImplementedError()


class StudentGroup(Base):

    __tablename__ = 'student_group'

    student_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)


class TeacherSubject(Base):

    __tablename__ = 'teacher_subject'

    teacher_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.id'), primary_key=True)


class UserType(Base):

    __tablename__ = 'user_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(15))


class User(DictMixin, Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(60))
    last_name = Column(String(120))

    user = Column(String(6), unique=True)
    type_id = Column(Integer, ForeignKey('user_type.id'))
    type = relationship(
        UserType,
        backref=backref('users', uselist=True, cascade='delete,all'))

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user': self.user,
            'type': self.type,
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


class Subject(DictMixin, Base):

    __tablename__ = 'subject'

    # Id field could be replaced by code field
    id = Column(Integer, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String(60))
    teachers = relationship('User', backref='subjects', secondary=TeacherSubject.__table__)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
        }


class Group(DictMixin, Base):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(
        Subject,
        backref=backref('groups', uselist=True, cascade='delete,all'))

    students = relationship('User', backref='groups', secondary=StudentGroup.__table__)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class MessageType(Base):

    DIRECT_MESSAGE = 'DIRECT_MESSAGE'
    GROUP_MESSAGE = 'GROUP_MESSAGE'
    SUBJECT_MESSAGE = 'SUBJECT_MESSAGE'

    __tablename__ = 'message_type'

    name = Column(String(20), primary_key=True)


class Message(DictMixin, Base):

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    body = Column(String(400))
    created_at = Column(DateTime)

    type = Column(String(20), ForeignKey('message_type.name'))

    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship(
        User,
        backref=backref('sent_messages', uselist=True, cascade='delete,all'),
        primaryjoin=sender_id == User.id)

    def __str__(self):
        return '<Message id={id}>'.format(id=self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.body,
        }

    __mapper_args__ = {'polymorphic_on': type}


class DirectMessage(Message):

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        User,
        backref=backref('received_direct_messages', uselist=True, cascade='delete,all'),
        primaryjoin=user_id == User.id)

    __mapper_args__ = {'polymorphic_identity': MessageType.DIRECT_MESSAGE}

    def to_dict(self):
        message = super(DirectMessage, self).to_dict()
        message.update({'user': self.user})
        return message


class GroupMessage(Message):

    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship(
        Group,
        backref=backref('received_group_messages', uselist=True, cascade='delete,all'))

    __mapper_args__ = {'polymorphic_identity': MessageType.GROUP_MESSAGE}

    def to_dict(self):
        message = super(DirectMessage, self).to_dict()
        message.update({'group': self.group})
        return message


class SubjectMessage(Message):

    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(
        Subject,
        backref=backref('received_subject_messages', uselist=True, cascade='delete,all'))

    __mapper_args__ = {'polymorphic_identity': MessageType.SUBJECT_MESSAGE}

    def to_dict(self):
        message = super(SubjectMessage, self).to_dict()
        message.update({'subject': self.subject})
        return message