from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Boolean, String, Date, DateTime, ForeignKey

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


student_group = Table(
    'student_group',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('person.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)

teacher_subject = Table(
    'teacher_subject',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('person.id')),
    Column('subject_id', Integer, ForeignKey('subject.id')),
)


class PersonType(Base):

    __tablename__ = 'person_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(15))


class Person(DictMixin, Base):

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(60))
    last_name = Column(String(120))

    user = Column(String(6), unique=True)
    type_id = Column(Integer, ForeignKey('person_type.id'))
    type = relationship(
        PersonType,
        backref=backref('persons', uselist=True, cascade='delete,all'))

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
    teachers = relationship('Person', backref='subjects', secondary=teacher_subject)


    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'groups': self.groups,
        }


class Group(DictMixin, Base):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(
        Subject,
        backref=backref('groups', uselist=True, cascade='delete,all'))

    students = relationship('Person', backref='groups', secondary=student_group)

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

    sender_id = Column(Integer, ForeignKey('person.id'))
    sender = relationship(
        Person,
        backref=backref('sent_messages', uselist=True, cascade='delete,all'),
        primaryjoin=sender_id == Person.id)

    def __str__(self):
        return '<Message id={id}>'.format(id=self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.body,
        }

    __mapper_args__ = {'polymorphic_on': type}


class DirectMessage(Message):

    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(
        Person,
        backref=backref('received_direct_messages', uselist=True, cascade='delete,all'),
        primaryjoin=person_id == Person.id)

    __mapper_args__ = {'polymorphic_identity': MessageType.DIRECT_MESSAGE}

    def to_dict(self):
        message = super(DirectMessage, self).to_dict()
        message.update({'person': self.person})
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