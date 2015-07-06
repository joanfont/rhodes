import urllib
from flask.ext.script import Command
import requests
from application.lib.models import User, UserType, Subject, TeacherSubject, Group, StudentGroup
from common.session import manager

BASE_URL = ''

GET_USERS_ENDPOINT = ''
GET_USER_TYPES_ENDPOINT = ''
GET_USER_DETAIL_ENDPOINT = ''
GET_SUBJECTS_ENDPOINT = ''
GET_GROUPS_ENDPOINT = ''

class ImportData(Command):

    def __init__(self, func=None):
        # Configure session

        self.req_session = requests.Session()
        self.db_session = manager.get('standalone')

        super(ImportData, self).__init__(func)

    @staticmethod
    def build_url(endpoint, params=None):
        url = '{}/{}'.format(BASE_URL, endpoint)
        if params:
            qs = urllib.urlencode(params)
            url = '{}?{}'.format(url, qs)

        return url

    def get_users(self):

        def _get_users(_page):
            url = self.build_url(GET_USERS_ENDPOINT, {'page': _page})
            data = self.req_session.get(url)
            return data.json()

        first_request = _get_users(1)
        count = first_request.get('count')
        items_per_page = first_request.get('items_per_page')
        pages = count / items_per_page if not count % items_per_page else (count / items_per_page) + 1
        pages = pages - 1 if pages > 1 else 0

        if pages > 1:
            users = []
            for page in xrange(2, pages):
                raw_users = _get_users(page)
                _users = raw_users.get('items')
                users.extend(_users)

        else:
            users = first_request.get('items')

        for user in users:
            u = User()
            u.first_name = user.get('first_name')
            u.last_name = user.get('last_name')
            u.type_id = user.get('type')
            u.user = user.get('user')

            self.db_session.add(u)
        self.db_session.commit()

    def get_user_types(self):

        types = self.req_session.get(GET_USER_TYPES_ENDPOINT)
        data = types.json()

        for _type in data:
            ut = UserType()
            ut.id = _type.get('id')
            ut.name = _type.get('name')
            self.db_session.add(ut)

        self.db_session.commit()

    def get_subjects(self):

        def _get_subjects(_page):
            url = self.build_url(GET_SUBJECTS_ENDPOINT, {'page': _page})
            data = self.req_session.get(url)
            return data.json()

        first_request = _get_subjects(1)
        count = first_request.get('count')
        items_per_page = first_request.get('items_per_page')
        pages = count / items_per_page if not count % items_per_page else (count / items_per_page) + 1
        pages = pages - 1 if pages > 1 else 0

        if pages > 1:
            subjects = []
            for page in xrange(2, pages):
                raw_subjects = _get_subjects(page)
                _subjects = raw_subjects.get('items')
                subjects.extend(_subjects)

        else:
            subjects = first_request.get('items')

        for subject in subjects:
            s = Subject()
            s.id = subject.get('id')
            s.code = subject.get('code')
            s.name = subject.get('name')

            self.db_session.add(s)

            for teacher in subject.get('teachers'):
                ts = TeacherSubject()
                ts.subject_id = s.id
                ts.teacher_id = teacher
                self.db_session.add(ts)

            self.db_session.commit()

            self.get_groups(s.id)

    def get_groups(self, subject):

        def _get_groups(_page, _subject):
            url = self.build_url(GET_SUBJECTS_ENDPOINT, {'page': _page, 'subject': _subject})
            data = self.req_session.get(url)
            return data.json()

        first_request = _get_groups(1, subject)
        count = first_request.get('count')
        items_per_page = first_request.get('items_per_page')
        pages = count / items_per_page if not count % items_per_page else (count / items_per_page) + 1
        pages = pages - 1 if pages > 1 else 0

        if pages > 1:
            groups = []
            for page in xrange(2, pages):
                raw_groups = _get_groups(page)
                _groups = raw_groups.get('items')
                groups.extend(_groups)

        else:
            groups = first_request.get('items')

        for group in groups:

            g = Group()
            g.id = group.get('id')
            g.name = group.get('name')

            self.db_session.add(g)

            for student in group.get('students'):
                sg = StudentGroup()
                sg.group_id = g.id
                sg.student_id = student

                self.db_session.add(sg)

            self.db_session()










