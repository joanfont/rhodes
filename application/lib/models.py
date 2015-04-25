from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, BigInteger

from common.helper import Helper
from common.session import manager
from common.auth import generate_auth_token

from config import config

from itertools import imap, chain

Base = declarative_base()


class SessionWrapper:

    def __init__(self):
        self.session = manager.get('flask')

    def add(self, obj):
        self.session.add(obj)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def query(self, *args):
        return self.session.query(*args)


class DictMixin(object):

    def to_dict(self, **kwargs):
        raise NotImplementedError()


class StudentGroup(Base):

    __tablename__ = 'student_group'
    __table_args__ = {'mysql_charset': 'utf8'}


    student_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)


class TeacherSubject(Base):

    __tablename__ = 'teacher_subject'
    __table_args__ = {'mysql_charset': 'utf8'}

    teacher_id = Column(BigInteger, ForeignKey('user.id'), primary_key=True)
    subject_id = Column(BigInteger, ForeignKey('subject.id'), primary_key=True)


class UserType(Base):

    __tablename__ = 'user_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    TEACHER = 1
    STUDENT = 2

    CHOICES = [TEACHER, STUDENT]

    id = Column(Integer, primary_key=True)
    name = Column(String(15))


class User(DictMixin, Base):

    __tablename__ = 'user'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(60))
    last_name = Column(String(120))

    user = Column(String(6), unique=True)
    password = Column(String(256))
    auth_token = Column(String(64))
    type_id = Column(Integer, ForeignKey('user_type.id'))
    type = relationship(
        UserType,
        backref=backref('users', uselist=True, cascade='delete,all'))

    def to_dict(self, **kwargs):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user': self.user,
            'type': self.type.name,
        }

    def is_teacher(self):
        return self.type.id == UserType.TEACHER

    def is_student(self):
        return self.type.id == UserType.STUDENT

    @property
    def full_name(self):
        return u'{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    def generate_auth_token(self):
        secret = config.PRIVATE_KEY
        message = "{id}{user}{type_id}".format(id=self.id, user=self.user, type_id=self.type_id)
        return generate_auth_token(message, secret)

    def get_subject_ids(self):

        def _get_teacher_subejct_ids():
            return map(lambda x: int(x.id), self.subjects)

        def _get_student_subjects_ids():
            return map(lambda x: int(x.subject.id), self.groups)

        dispatcher = {
            UserType.TEACHER: _get_teacher_subejct_ids,
            UserType.STUDENT: _get_student_subjects_ids,
        }

        get_subjects_ids_fnx = dispatcher.get(self.type_id)

        subjects = get_subjects_ids_fnx()
        return subjects

    def get_groups_ids(self):

        def _get_teacher_groups_ids():

            def _get_subject_groups(subject):
                return imap(lambda x: int(x.id), subject.groups)

            subject_goups = imap(_get_subject_groups, self.subjects)

            return list(chain(subject_goups))

        def _get_student_groups_ids():
            return map(lambda x: int(x.id), self.groups)

        dispatcher = {
            UserType.TEACHER: _get_teacher_groups_ids,
            UserType.STUDENT: _get_student_groups_ids,
        }

        get_groups_ids_fnx = dispatcher.get(self.type_id)

        groups = get_groups_ids_fnx()
        return groups


class Subject(DictMixin, Base):

    __tablename__ = 'subject'
    __table_args__ = {'mysql_charset': 'utf8'}

    # Id field could be replaced by code field
    id = Column(BigInteger, primary_key=True)
    code = Column(Integer, unique=True)
    name = Column(String(60))
    teachers = relationship('User', backref='subjects', secondary=TeacherSubject.__table__)

    def to_dict(self, **kwargs):
        base = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
        }

        if kwargs.get('with_group'):
            base.update({'group': self.group.to_dict(**kwargs)})

        if kwargs.get('with_groups'):
            groups = map(lambda x: x.to_dict(**kwargs), self.groups)
            base.update({'groups': groups})

        return base


class Group(DictMixin, Base):

    __tablename__ = 'group'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(BigInteger, primary_key=True)
    name = Column(String(60))
    subject_id = Column(BigInteger, ForeignKey('subject.id'))
    subject = relationship(
        Subject,
        backref=backref('groups', uselist=True, cascade='delete,all'))

    students = relationship('User', backref='groups', secondary=StudentGroup.__table__)

    def to_dict(self, **kwargs):
        return {
            'id': self.id,
            'name': self.name,
        }


class MessageType(Base):

    DIRECT_MESSAGE = 1
    GROUP_MESSAGE = 2
    SUBJECT_MESSAGE = 3

    CHOICES = [DIRECT_MESSAGE, GROUP_MESSAGE, SUBJECT_MESSAGE]

    __tablename__ = 'message_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    name = Column(String(20))


class MessageBody(Base):

    MAX_LENGTH = config.MESSAGE_MAX_LENGTH

    __tablename__ = 'message_body'

    id = Column(BigInteger, primary_key=True)
    content = Column(String(MAX_LENGTH))


class Message(DictMixin, Base):

    __tablename__ = 'message'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)

    type = Column(Integer, ForeignKey('message_type.id'))

    sender_id = Column(BigInteger, ForeignKey('user.id'))
    sender = relationship(
        User,
        backref=backref('sent_messages', uselist=True, cascade='delete,all'),
        primaryjoin=sender_id == User.id)

    body_id = Column(BigInteger, ForeignKey('message_body.id'))
    body = relationship(
        MessageBody,
        backref=backref('message', uselist=True, cascade='delete,all'),
        primaryjoin=body_id == MessageBody.id)

    def to_dict(self, **kwargs):
        return {
            'id': self.id,
            'body': self.body.content,
            'created_at': Helper.datetime_format(self.created_at),
            'sender': self.sender.to_dict(**kwargs)
        }

    __mapper_args__ = {'polymorphic_on': type}


class DirectMessage(Message):

    user_id = Column(BigInteger, ForeignKey('user.id'))
    user = relationship(
        User,
        backref=backref('received_direct_messages', uselist=True, cascade='delete,all'),
        primaryjoin=user_id == User.id)

    __mapper_args__ = {'polymorphic_identity': MessageType.DIRECT_MESSAGE}


class GroupMessage(Message):

    group_id = Column(BigInteger, ForeignKey('group.id'))
    group = relationship(
        Group,
        backref=backref('received_group_messages', uselist=True, cascade='delete,all'))

    __mapper_args__ = {'polymorphic_identity': MessageType.GROUP_MESSAGE}


class SubjectMessage(Message):

    subject_id = Column(BigInteger, ForeignKey('subject.id'))
    subject = relationship(
        Subject,
        backref=backref('received_subject_messages', uselist=True, cascade='delete,all'))

    __mapper_args__ = {'polymorphic_identity': MessageType.SUBJECT_MESSAGE}
