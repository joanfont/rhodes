from collections import OrderedDict


class BaseEntity(object):

    def __init__(self):
        super(BaseEntity, self).__init__()

    def to_dict(self):
        raise NotImplementedError()


class PaginatedEntity(BaseEntity):

    objects = []
    total = 0
    count = 0

    def __init__(self, objects=[], total=0, count=0, **options):

        if objects:
            self.objects = map(lambda x: x.to_dict(**options), objects)

        if total:
            self.total = total

        if count:
            self.count = count

    def to_dict(self):
        return {
            'total': self.total,
            'count': self.count,
            'objects': self.objects
        }


class PaginatedMessagesEntity(PaginatedEntity):

    more = False

    def __init__(self, objects=[], total=0, count=0, more=False, **options):
        super(PaginatedMessagesEntity, self).__init__(objects, total, count, **options)

        if more:
            self.more = more

    def to_dict(self):
        super_dict = super(PaginatedMessagesEntity, self).to_dict()
        messages = super_dict.pop('objects', [])

        result = OrderedDict((
            ('count', super_dict.get('count')),
            ('total', super_dict.get('total')),
            ('more', self.more),
            ('messages', messages)
        ))

        return result


class Conversation(dict):

    def __init__(self, user={}, last_message={}):
        if user:
            user = user.to_dict()
        if last_message:
            last_message = last_message.to_dict()

        super(Conversation, self).__init__(user=user, last_message=last_message)


class Subject(BaseEntity):

    def __init__(self, _id, name, code, groups):

        self.id = _id
        self.name = name
        self.code = code
        self.groups = groups

    def to_dict(self, **kwargs):
        groups = map(lambda x: x.to_dict(**kwargs), self.groups)
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'groups': groups
        }


class Group(BaseEntity):

    def __init__(self, _id, name):

        self.id = _id
        self.name = name

    def to_dict(self, **kwargs):
        return {
            'id': self.id,
            'name': self.name
        }
